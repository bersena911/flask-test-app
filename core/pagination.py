from functools import wraps

import pydantic
from flask import request
from pydantic import Extra


class BasePaginate(pydantic.BaseModel):
    total_count: int
    limit: int
    offset: int


class Paginate:
    def __class_getitem__(cls, item):
        return pydantic.create_model(
            f"Paginate{item.__name__}", items=(list[item], ...), __base__=BasePaginate
        )


class PaginateSchema(pydantic.BaseModel, extra=Extra.ignore):
    limit: int = 15
    offset: int = 0


def paginate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validated_pagination = PaginateSchema(**request.args)
        kwargs["limit"] = validated_pagination.limit
        kwargs["offset"] = validated_pagination.offset
        return f(*args, **kwargs)

    return decorated_function
