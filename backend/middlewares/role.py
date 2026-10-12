from functools import wraps
from flask import g
from utils.response import fail


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(g, "current_user", None)
            if not user or user.role not in roles:
                return fail(10003)
            return f(*args, **kwargs)
        return wrapper
    return decorator