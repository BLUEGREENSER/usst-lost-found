import json
import datetime
from flask import Blueprint, request, g, current_app
from extensions.db import db
from models.lost_item import LostItem
from models.match_record import MatchRecord
from models.claim_record import ClaimRecord
from models.user import User
from utils.response import success, fail, BizError
from utils.desensitize import desensitize_email, desensitize_student_id, desensitize_name
from middlewares.auth import login_required
from services.notify_service import notify
from services.match_engine import invalidate_matches

bp = Blueprint("lost", __name__)


@bp.route("", methods=["POST"])
@bp.route("/", methods=["POST"])
@login_required
def publish_lost():
    data = request.get_json(silent=True) or {}
    name = data.get("name", "").strip()
    category = data.get("category", "").strip()
    lost_time = data.get("lost_time", "").strip()
    location = data.get("location", "").strip()
    description = data.get("description", "").strip()
    image_urls = data.get("image_urls", [])
    contact_visibility = data.get("contact_visibility", "仅匹配可见")

    if not name or not category or not lost_time or not location:
        return fail(10001, "缺少必填字段")
    if category not in current_app.config["ITEM_CATEGORIES"]:
        return fail(10001, "物品类别不合法")
    if len(image_urls) > current_app.config["IMAGE_MAX_COUNT"]:
        return fail(10007, f"图片数量超过{current_app.config['IMAGE_MAX_COUNT']}张")
    if contact_visibility not in current_app.config["CONTACT_VISIBILITIES"]:
        contact_visibility = "仅匹配可见"

    item = LostItem(
        publisher_id=g.current_user.id,
        name=name,
        category=category,
        description=description,
        lost_time=lost_time,
        location=location,
        contact_visibility=contact_visibility,
        image_urls=json.dumps(image_urls, ensure_ascii=False),
        status="待审核",
    )
    db.session.add(item)
    db.session.commit()

    admins = User.query.filter_by(role="admin", status="active").all()
    for a in admins:
        notify(a.id, "audit", f"有新的失物待审核：{name}", "/admin/audit")

    return success({"lost_id": item.id, "status": item.status}, "发布成功，等待审核")


@bp.route("/mine", methods=["GET"])
@login_required
def my_lost_list():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    status = request.args.get("status")
    category = request.args.get("category")

    query = LostItem.query.filter_by(publisher_id=g.current_user.id)
    if status:
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
    total = query.count()
    items = query.order_by(LostItem.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return success({"list": [i.to_dict() for i in items], "total": total})


@bp.route("/<int:item_id>", methods=["GET"])
def lost_detail(item_id):
    item = LostItem.query.get(item_id)
    if not item:
        return fail(10004)
    is_self = hasattr(g, "current_user") and g.current_user.id == item.publisher_id
    if not is_self and item.status != "已发布":
        return fail(10004)

    data = item.to_dict()
    if is_self:
        publisher = User.query.get(item.publisher_id)
        data["publisher"] = publisher.to_dict() if publisher else None
    else:
        data["publisher"] = _desensitized_publisher(item)
    return success(data)


def _desensitized_publisher(item):
    publisher = User.query.get(item.publisher_id)
    if not publisher:
        return None
    vis = item.contact_visibility
    if vis == "公开":
        return publisher.to_dict()
    info = {"name": desensitize_name(publisher.name)}
    if vis == "仅登录可见" and hasattr(g, "current_user") and g.current_user:
        info["email"] = desensitize_email(publisher.email)
        info["student_id"] = desensitize_student_id(publisher.student_id)
    return info


@bp.route("/<int:item_id>", methods=["PUT"])
@login_required
def edit_lost(item_id):
    item = LostItem.query.get(item_id)
    if not item:
        return fail(10004)
    if item.publisher_id != g.current_user.id:
        return fail(10003)
    if item.status not in ("待审核", "已发布", "已驳回"):
        return fail(10007, "当前状态不可编辑")

    data = request.get_json(silent=True) or {}
    for field in ["name", "category", "description", "lost_time", "location", "contact_visibility"]:
        if field in data and data[field] is not None:
            setattr(item, field, data[field])
    if "image_urls" in data:
        item.image_urls = json.dumps(data["image_urls"], ensure_ascii=False)
    item.status = "待审核"
    item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.session.commit()
    return success(item.to_dict(), "已更新，等待审核")


@bp.route("/<int:item_id>", methods=["DELETE"])
@login_required
def delete_lost(item_id):
    item = LostItem.query.get(item_id)
    if not item:
        return fail(10004)
    if item.publisher_id != g.current_user.id:
        return fail(10003)

    pending_matches = MatchRecord.query.filter_by(lost_id=item_id, status="待确认").count()
    pending_claims = ClaimRecord.query.filter(
        ClaimRecord.match_id.in_(
            db.session.query(MatchRecord.id).filter_by(lost_id=item_id)
        ),
        ClaimRecord.status == "进行中",
    ).count()
    if pending_matches or pending_claims:
        return fail(10007, "存在进行中的匹配或认领，无法撤回")

    item.status = "已关闭"
    item.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.session.commit()
    invalidate_matches(lost_id=item_id)
    return success(None, "已撤回")