import datetime
from flask import Blueprint, request, g, current_app
from extensions.db import db
from models.match_record import MatchRecord
from models.claim_record import ClaimRecord
from models.lost_item import LostItem
from models.found_item import FoundItem
from utils.response import success, fail
from middlewares.auth import login_required
from services.verify_code import generate_and_store_code, verify_code, check_resend_limit
from services.notify_service import notify
from services.match_engine import invalidate_matches

bp = Blueprint("claim", __name__)


@bp.route("", methods=["POST"])
@bp.route("/", methods=["POST"])
@login_required
def create_claim():
    data = request.get_json(silent=True) or {}
    match_id = data.get("match_id")
    m = MatchRecord.query.get(match_id)
    if not m:
        return fail(10004)
    if m.status != "已确认":
        return fail(10007, "匹配未确认，无法发起认领")

    lost = LostItem.query.get(m.lost_id)
    if not lost or lost.publisher_id != g.current_user.id:
        return fail(10003, "仅失主可发起认领")

    existing = ClaimRecord.query.filter_by(match_id=match_id, status="进行中").first()
    if existing:
        return fail(10005, "该匹配已有进行中的认领")
    existing_done = ClaimRecord.query.filter_by(match_id=match_id, status="已完成").first()
    if existing_done:
        return fail(10005, "该匹配已完成认领")

    found = FoundItem.query.get(m.found_id)
    claim = ClaimRecord(
        match_id=match_id,
        loser_id=lost.publisher_id,
        finder_id=found.publisher_id,
        verify_code_hash="",
        code_salt="",
        code_status="已生成",
        code_expire_at=(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)).isoformat(),
        status="进行中",
    )
    db.session.add(claim)
    db.session.commit()

    code = generate_and_store_code(claim.id)
    if not code:
        return fail(20001, "校验码生成失败")

    notify(claim.loser_id, "claim", f"认领已发起，校验码：{code}，请妥善保管", f"/claims/{claim.id}")
    notify(claim.finder_id, "claim", "有失主发起了认领，请输入校验码确认", f"/claims/{claim.id}")

    return success({"claim_id": claim.id, "verify_code": code}, "认领已发起，校验码已通过站内消息发送")


@bp.route("/<int:claim_id>/verify", methods=["POST"])
@login_required
def verify_claim_code(claim_id):
    data = request.get_json(silent=True) or {}
    code_input = data.get("verify_code", "")
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return fail(10004)
    if claim.finder_id != g.current_user.id:
        return fail(10003, "仅拾到者可核验校验码")

    ok, err_code, msg = verify_code(claim_id, code_input)
    if not ok:
        return fail(err_code, msg)

    try:
        m = MatchRecord.query.get(claim.match_id)
        lost = LostItem.query.get(m.lost_id)
        found = FoundItem.query.get(m.found_id)

        lost.status = "已认领"
        found.status = "已认领"
        m.status = "已确认"
        claim.status = "已完成"
        claim.code_status = "已使用"
        claim.completed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

        other_matches = MatchRecord.query.filter(
            MatchRecord.id != m.id,
            db.or_(MatchRecord.lost_id == m.lost_id, MatchRecord.found_id == m.found_id),
            MatchRecord.status == "待确认",
        ).all()
        for om in other_matches:
            om.status = "已失效"

        db.session.commit()
        notify(claim.loser_id, "claim", "认领完成！", f"/claims/{claim.id}")
        notify(claim.finder_id, "claim", "认领完成！", f"/claims/{claim.id}")
        return success(claim.to_dict(), "核验成功，认领完成")
    except Exception as e:
        db.session.rollback()
        return fail(20001, f"认领事务失败: {str(e)}")


@bp.route("/<int:claim_id>/cancel", methods=["POST"])
@login_required
def cancel_claim(claim_id):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return fail(10004)
    if claim.loser_id != g.current_user.id:
        return fail(10003, "仅失主可取消认领")
    if claim.status != "进行中":
        return fail(10007, "认领状态不允许")

    claim.status = "已取消"
    claim.code_status = "已失效"
    db.session.commit()
    notify(claim.finder_id, "claim", "失主已取消认领", f"/claims/{claim_id}")
    return success(None, "已取消")


@bp.route("/<int:claim_id>/resend", methods=["POST"])
@login_required
def resend_code(claim_id):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return fail(10004)
    if claim.loser_id != g.current_user.id:
        return fail(10003, "仅失主可重发校验码")
    if claim.status != "进行中":
        return fail(10007, "认领状态不允许")

    if not check_resend_limit(claim_id):
        return fail(10006, "重发次数超限，请稍后再试")

    code = generate_and_store_code(claim_id)
    if not code:
        return fail(20001, "校验码生成失败")
    notify(claim.loser_id, "claim", f"新校验码：{code}", f"/claims/{claim_id}")
    notify(claim.finder_id, "claim", "失主重发了校验码，请注意查收", f"/claims/{claim_id}")
    return success({"verify_code": code}, "校验码已重发")


@bp.route("/<int:claim_id>", methods=["GET"])
@login_required
def claim_detail(claim_id):
    claim = ClaimRecord.query.get(claim_id)
    if not claim:
        return fail(10004)
    if claim.loser_id != g.current_user.id and claim.finder_id != g.current_user.id:
        return fail(10003)
    data = claim.to_dict()
    m = MatchRecord.query.get(claim.match_id)
    data["match"] = m.to_dict() if m else None
    if m:
        data["lost"] = LostItem.query.get(m.lost_id).to_dict() if LostItem.query.get(m.lost_id) else None
        data["found"] = FoundItem.query.get(m.found_id).to_dict() if FoundItem.query.get(m.found_id) else None
    data["is_loser"] = claim.loser_id == g.current_user.id
    data["is_finder"] = claim.finder_id == g.current_user.id
    return success(data)