from functools import wraps

from flask import request


def validate_post_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = f.__annotations__["data"]
        validated_data = validator(**request.json)
        kwargs["data"] = validated_data
        return f(*args, **kwargs)

    return decorated_function
