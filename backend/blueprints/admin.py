import datetime
from flask import Blueprint, request, g, current_app
from extensions.db import db
from models.user import User
from models.lost_item import LostItem
from models.found_item import FoundItem
from models.match_record import MatchRecord
from models.claim_record import ClaimRecord
from models.audit_log import AuditLog
from utils.response import success, fail
from middlewares.auth import login_required
from middlewares.role import role_required
from services.match_engine import trigger_match_for_lost, trigger_match_for_found, invalidate_matches
from services.notify_service import notify

bp = Blueprint("admin", __name__)


@bp.route("/audit/list", methods=["GET"])
@login_required
@role_required("admin")
def audit_list():
    item_type = request.args.get("type", "lost")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))

    if item_type == "found":
        query = FoundItem.query.filter_by(status="待审核")
        order_field = FoundItem.created_at
    else:
        query = LostItem.query.filter_by(status="待审核")
        order_field = LostItem.created_at

    total = query.count()
    items = query.order_by(order_field.desc()).offset((page - 1) * page_size).limit(page_size).all()
    result_list = []
    for item in items:
        d = item.to_dict()
        pub = User.query.get(item.publisher_id)
        d["publisher_name"] = pub.name if pub else ""
        result_list.append(d)
    return success({"list": result_list, "total": total})


@bp.route("/audit/<item_type>/<int:item_id>/approve", methods=["POST"])
@login_required
@role_required("admin")
def approve(item_type, item_id):
    if item_type == "found":
        item = FoundItem.query.get(item_id)
        if not item:
            return fail(10004)
        if item.publisher_id == g.current_user.id:
            return fail(10003, "不能审核自己发布的内容")
        item.status = "已发布"
        item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        db.session.commit()
        notify(item.publisher_id, "audit", f"您的拾物已审核通过：{item.name}", f"/found/{item_id}")
        trigger_match_for_found(item_id)
    else:
        item = LostItem.query.get(item_id)
        if not item:
            return fail(10004)
        if item.publisher_id == g.current_user.id:
            return fail(10003, "不能审核自己发布的内容")
        item.status = "已发布"
        item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        db.session.commit()
        notify(item.publisher_id, "audit", f"您的失物已审核通过：{item.name}", f"/lost/{item_id}")
        trigger_match_for_lost(item_id)

    _add_audit_log(f"approve_{item_type}", item_id)
    return success(None, "已审核通过")


@bp.route("/audit/<item_type>/<int:item_id>/reject", methods=["POST"])
@login_required
@role_required("admin")
def reject(item_type, item_id):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", "").strip()
    if not reason:
        return fail(10001, "请填写驳回理由")

    if item_type == "found":
        item = FoundItem.query.get(item_id)
    else:
        item = LostItem.query.get(item_id)
    if not item:
        return fail(10004)

    item.status = "已驳回"
    item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.session.commit()
    notify(item.publisher_id, "audit", f"您的{item_type == 'found' and '拾物' or '失物'}被驳回：{reason}", "")
    _add_audit_log(f"reject_{item_type}", item_id, detail=reason)
    return success(None, "已驳回")


@bp.route("/items/<item_type>/<int:item_id>/takedown", methods=["POST"])
@login_required
@role_required("admin")
def takedown(item_type, item_id):
    data = request.get_json(silent=True) or {}
    reason = data.get("reason", "").strip()
    if item_type == "found":
        item = FoundItem.query.get(item_id)
        invalidate_matches(found_id=item_id)
    else:
        item = LostItem.query.get(item_id)
        invalidate_matches(lost_id=item_id)
    if not item:
        return fail(10004)
    item.status = "已关闭"
    item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.session.commit()
    notify(item.publisher_id, "audit", f"您的物品已被下架：{reason}", "")
    _add_audit_log(f"takedown_{item_type}", item_id, detail=reason)
    return success(None, "已下架")


@bp.route("/users/<int:user_id>/enable", methods=["POST"])
@login_required
@role_required("admin")
def enable_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return fail(10004)
    user.status = "active"
    db.session.commit()
    _add_audit_log("enable_user", user_id)
    return success(None, "已启用")


@bp.route("/users/<int:user_id>/disable", methods=["POST"])
@login_required
@role_required("admin")
def disable_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return fail(10004)
    if user.id == g.current_user.id:
        return fail(10007, "不能禁用自己")
    user.status = "disabled"
    db.session.commit()
    _add_audit_log("disable_user", user_id)
    return success(None, "已禁用")


@bp.route("/users", methods=["GET"])
@login_required
@role_required("admin")
def list_users():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))
    query = User.query
    total = query.count()
    users = query.order_by(User.registered_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"list": [u.to_dict() for u in users], "total": total})


@bp.route("/stats", methods=["GET"])
@login_required
@role_required("admin")
def stats():
    period = request.args.get("period", "day")
    now = datetime.datetime.now(datetime.timezone.utc)

    if period == "week":
        start = (now - datetime.timedelta(days=7)).isoformat()
    elif period == "month":
        start = (now - datetime.timedelta(days=30)).isoformat()
    else:
        start = (now - datetime.timedelta(days=1)).isoformat()

    publish_count = LostItem.query.filter(LostItem.created_at >= start).count() + FoundItem.query.filter(FoundItem.created_at >= start).count()
    match_count = MatchRecord.query.filter(MatchRecord.created_at >= start).count()
    claim_count = ClaimRecord.query.filter(ClaimRecord.created_at >= start).count()
    audit_pending_count = LostItem.query.filter_by(status="待审核").count() + FoundItem.query.filter_by(status="待审核").count()

    return success({
        "publish_count": publish_count,
        "match_count": match_count,
        "claim_count": claim_count,
        "audit_pending_count": audit_pending_count,
    })


def _add_audit_log(action, target_id, detail=None):
    log = AuditLog(
        operator_id=g.current_user.id,
        action=action,
        target_type=action.split("_")[-1] if "_" in action else "item",
        target_id=target_id,
        detail=detail,
    )
    db.session.add(log)
    db.session.commit()