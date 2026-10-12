from functools import wraps
from flask import g, request
from utils.response import fail


def ownership_required(model, id_param="id", owner_field="publisher_id"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resource_id = kwargs.get(id_param)
            resource = model.query.get(resource_id)
            if not resource:
                return fail(10004)
            if getattr(resource, owner_field) != g.current_user.id:
                return fail(10003)
            g.resource = resource
            return f(*args, **kwargs)
        return wrapper
    return decorator