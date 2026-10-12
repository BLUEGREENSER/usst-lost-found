import json
from flask import Blueprint, request, g
from extensions.db import db
from models.match_record import MatchRecord
from models.lost_item import LostItem
from models.found_item import FoundItem
from utils.response import success, fail
from middlewares.auth import login_required
from services.notify_service import notify

bp = Blueprint("match", __name__)


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
@login_required
def list_matches():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    status = request.args.get("status")

    lost_ids = db.session.query(LostItem.id).filter_by(publisher_id=g.current_user.id).subquery()
    found_ids = db.session.query(FoundItem.id).filter_by(publisher_id=g.current_user.id).subquery()

    query = MatchRecord.query.filter(
        db.or_(MatchRecord.lost_id.in_(lost_ids), MatchRecord.found_id.in_(found_ids))
    )
    if status:
        query = query.filter_by(status=status)
    total = query.count()
    items = query.order_by(MatchRecord.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result_list = []
    for m in items:
        d = m.to_dict()
        d["dimensions"] = json.loads(m.dimensions) if m.dimensions else None
        lost = LostItem.query.get(m.lost_id)
        found = FoundItem.query.get(m.found_id)
        d["lost"] = lost.to_dict() if lost else None
        d["found"] = found.to_dict() if found else None
        result_list.append(d)
    return success({"list": result_list, "total": total})


@bp.route("/<int:match_id>/confirm", methods=["POST"])
@login_required
def confirm_match(match_id):
    m = MatchRecord.query.get(match_id)
    if not m:
        return fail(10004)
    if m.status != "待确认":
        return fail(10007, "匹配状态不允许")

    lost = LostItem.query.get(m.lost_id)
    found = FoundItem.query.get(m.found_id)
    is_loser = lost and lost.publisher_id == g.current_user.id
    is_finder = found and found.publisher_id == g.current_user.id
    if not (is_loser or is_finder):
        return fail(10003)

    if is_loser:
        m.lost_confirmed = 1
    if is_finder:
        m.found_confirmed = 1

    if m.lost_confirmed and m.found_confirmed:
        m.status = "已确认"
        lost.status = "已匹配"
        found.status = "已匹配"
        notify(lost.publisher_id, "match", "匹配已确认，可以发起认领", "/claims")
        notify(found.publisher_id, "match", "匹配已确认，失主可发起认领", "/matches")

    db.session.commit()
    return success(m.to_dict(), "已确认")


@bp.route("/<int:match_id>/reject", methods=["POST"])
@login_required
def reject_match(match_id):
    m = MatchRecord.query.get(match_id)
    if not m:
        return fail(10004)
    if m.status != "待确认":
        return fail(10007, "匹配状态不允许")

    lost = LostItem.query.get(m.lost_id)
    found = FoundItem.query.get(m.found_id)
    is_loser = lost and lost.publisher_id == g.current_user.id
    is_finder = found and found.publisher_id == g.current_user.id
    if not (is_loser or is_finder):
        return fail(10003)

    m.status = "已拒绝"
    db.session.commit()
    return success(None, "已拒绝")