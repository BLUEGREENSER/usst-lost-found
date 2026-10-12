import os
import uuid
from flask import Blueprint, request, current_app
from extensions.db import db
from models.image import Image
from utils.response import success, fail
from middlewares.auth import login_required

bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MAGICS = {b"\xff\xd8\xff": "jpg", b"\x89PNG": "png"}


@bp.route("/image", methods=["POST"])
@login_required
def upload_image():
    if "file" not in request.files:
        return fail(10001, "未选择文件")
    file = request.files["file"]
    if not file.filename:
        return fail(10001, "未选择文件")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return fail(10001, "仅支持jpg/png格式")

    header = file.read(4)
    file.seek(0)
    if not any(header.startswith(magic) for magic in [b"\xff\xd8\xff", b"\x89PNG"]):
        return fail(10001, "文件内容与格式不符")

    max_size = current_app.config["IMAGE_MAX_SIZE_MB"] * 1024 * 1024
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    if size > max_size:
        return fail(10001, f"图片大小超过{current_app.config['IMAGE_MAX_SIZE_MB']}MB")

    filename = uuid.uuid4().hex + ext
    storage_dir = current_app.config["IMAGE_STORAGE_DIR"]
    os.makedirs(storage_dir, exist_ok=True)
    filepath = os.path.join(storage_dir, filename)
    file.save(filepath)

    url = current_app.config["IMAGE_URL_PREFIX"] + "/" + filename
    img = Image(owner_type="temp", owner_id=0, url=url)
    db.session.add(img)
    db.session.commit()

    return success({"url": url}, "上传成功")