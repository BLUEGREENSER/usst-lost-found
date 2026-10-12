import re
import datetime
from flask import Blueprint, request, g
from extensions.db import db
from extensions.jwt import generate_token
from models.user import User
from utils.response import success, fail, BizError
from utils.security import hash_password, verify_password
from middlewares.auth import login_required

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    student_id = data.get("student_id", "").strip()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    domain = _get_domain()
    if not email.endswith(domain):
        return fail(10001, f"请使用学校邮箱（{domain}）")
    if not re.match(r"^\d{8,12}$", student_id):
        return fail(10001, "学号需为8-12位数字")
    if not name or len(name) > 20:
        return fail(10001, "姓名不合法")
    if len(password) < 8 or not re.search(r"[a-zA-Z]", password) or not re.search(r"\d", password):
        return fail(10001, "密码至少8位且含字母与数字")

    if User.query.filter_by(email=email).first():
        return fail(10005, "该邮箱已注册")
    if User.query.filter_by(student_id=student_id).first():
        return fail(10005, "该学号已注册")

    pwd_hash, salt = hash_password(password)
    user = User(
        student_id=student_id,
        name=name,
        email=email,
        password_hash=pwd_hash,
        salt=salt,
        role="student",
        status="active",
    )
    db.session.add(user)
    db.session.commit()
    return success({"user_id": user.id}, "注册成功")


def _get_domain():
    from flask import current_app
    return current_app.config["SCHOOL_EMAIL_DOMAIN"]


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    account = data.get("account", "").strip() or data.get("email", "").strip()
    password = data.get("password", "")

    if not account:
        return fail(10001, "请输入账号")

    user = User.query.filter_by(email=account).first()
    if not user:
        user = User.query.filter_by(student_id=account).first()
    if not user:
        user = User.query.filter_by(name=account).first()
    if not user:
        return fail(10001, "账号或密码错误")
    if user.status != "active":
        return fail(10003, "账号已被禁用")
    if not verify_password(password, user.password_hash, user.salt):
        return fail(10001, "账号或密码错误")

    token = generate_token(user.id, user.role)
    user.last_login_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    db.session.commit()

    from flask import current_app
    expires_in = current_app.config["JWT_EXPIRE_DAYS"] * 86400
    return success({
        "token": token,
        "expires_in": expires_in,
        "user": user.to_dict(),
    }, "登录成功")


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    return success(None, "登出成功")