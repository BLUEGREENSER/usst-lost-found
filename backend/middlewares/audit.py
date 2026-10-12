from functools import wraps
from flask import g, request
from extensions.db import db
from models.audit_log import AuditLog


def audit_log(action):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            try:
                log = AuditLog(
                    operator_id=g.current_user.id,
                    action=action,
                    target_type=request.path,
                    target_id=kwargs.get("id"),
                    result="success",
                )
                db.session.add(log)
                db.session.commit()
            except Exception:
                db.session.rollback()
            return result
        return wrapper
    return decorator