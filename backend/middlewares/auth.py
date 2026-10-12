from functools import wraps
from flask import request, g
from extensions.jwt import decode_token
from utils.response import fail
from models.user import User


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return fail(10002)
        token = auth_header[7:]
        try:
            payload = decode_token(token)
        except Exception:
            return fail(10002)
        user = User.query.get(payload.get("user_id"))
        if not user or user.status != "active":
            return fail(10003)
        g.current_user = user
        return f(*args, **kwargs)
    return wrapper