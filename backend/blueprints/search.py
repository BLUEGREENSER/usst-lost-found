from flask import Blueprint, request, g, current_app
from extensions.db import db
from models.lost_item import LostItem
from models.found_item import FoundItem
from models.user import User
from utils.response import success, fail
from utils.desensitize import desensitize_email, desensitize_student_id, desensitize_name

bp = Blueprint("search", __name__)


@bp.route("", methods=["GET"])
@bp.route("/", methods=["GET"])
def search():
    item_type = request.args.get("type", "lost")
    keyword = request.args.get("keyword", "").strip()
    category = request.args.get("category", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    location = request.args.get("location", "").strip()
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", current_app.config["PAGE_SIZE_DEFAULT"]))
    sort = request.args.get("sort", "time")

    if page_size > current_app.config["PAGE_SIZE_MAX"]:
        page_size = current_app.config["PAGE_SIZE_MAX"]

    if item_type == "found":
        query = FoundItem.query.filter_by(status="已发布")
        time_field = FoundItem.found_time
    else:
        query = LostItem.query.filter_by(status="已发布")
        time_field = LostItem.lost_time

    if keyword:
        like = f"%{keyword}%"
        query = query.filter(db.or_(LostItem.name.like(like), LostItem.description.like(like))) if item_type == "lost" \
            else query.filter(db.or_(FoundItem.name.like(like), FoundItem.description.like(like)))
    if category:
        query = query.filter_by(category=category)
    if start_date:
        query = query.filter(time_field >= start_date)
    if end_date:
        query = query.filter(time_field <= end_date)
    if location:
        query = query.filter(LostItem.location.like(f"%{location}%") if item_type == "lost" else FoundItem.location.like(f"%{location}%"))

    total = query.count()
    if sort == "relevance" and keyword:
        query = query.order_by(time_field.desc())
    else:
        query = query.order_by(LostItem.created_at.desc() if item_type == "lost" else FoundItem.created_at.desc())

    items = query.offset((page - 1) * page_size).limit(page_size).all()
    result_list = []
    for item in items:
        d = item.to_dict()
        d["publisher"] = _desensitized_publisher(item)
        result_list.append(d)
    return success({"list": result_list, "total": total})


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