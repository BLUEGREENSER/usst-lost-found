from flask import Blueprint, request, g
from models.notification import Notification
from utils.response import success, fail
from middlewares.auth import login_required
from extensions.db import db

bp = Blueprint("notify", __name__)


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
@login_required
def list_notifications():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    is_read = request.args.get("is_read")

    query = Notification.query.filter_by(recipient_id=g.current_user.id, is_archived=0)
    if is_read is not None and is_read != "":
        query = query.filter_by(is_read=int(is_read))
    total = query.count()
    items = query.order_by(Notification.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"list": [n.to_dict() for n in items], "total": total})


@bp.route("/unread-count", methods=["GET"])
@login_required
def unread_count():
    count = Notification.query.filter_by(recipient_id=g.current_user.id, is_read=0, is_archived=0).count()
    return success({"count": count})


@bp.route("/<int:nid>/read", methods=["POST"])
@login_required
def mark_read(nid):
    n = Notification.query.get(nid)
    if not n or n.recipient_id != g.current_user.id:
        return fail(10004)
    n.is_read = 1
    db.session.commit()
    return success(None, "已标记已读")


@bp.route("/read-all", methods=["POST"])
@login_required
def mark_all_read():
    Notification.query.filter_by(recipient_id=g.current_user.id, is_read=0).update({"is_read": 1})
    db.session.commit()
    return success(None, "全部已读")