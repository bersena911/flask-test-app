from flask import g, Blueprint

from core.errors import HTTPException
from core.jwt import auth_required
from db.utils import (
    check_if_user_is_superuser,
    get_role_by_name,
    create_role,
    get_roles,
    get_user_roles,
)
from settings import API_V1_STR

roles_router = Blueprint("roles", __name__)


@roles_router.route(f"{API_V1_STR}/roles/", methods=["POST"])
@auth_required
def route_roles_post(name=None):
    current_user = g.current_user

    if not check_if_user_is_superuser(current_user):
        raise HTTPException(400, "Not a superuser")

    role = get_role_by_name(name)
    if role:
        raise HTTPException(400, f"The role: {name} already exists in the system")
    role = create_role(name)
    return role


@roles_router.route(f"{API_V1_STR}/roles/", methods=["GET"])
@auth_required
def route_roles_get():
    current_user = g.current_user

    if check_if_user_is_superuser(current_user):
        return get_roles()
    else:
        return get_user_roles(current_user)
