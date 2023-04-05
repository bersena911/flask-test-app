from flask import g, Blueprint, request, jsonify

from core.errors import HTTPException
from core.jwt import auth_required, superuser_required
from db.utils import (
    check_if_user_is_superuser,
    get_role_by_name,
    create_role,
    get_roles,
    get_user_roles,
)
from schemas.role import Role
from settings import API_V1_STR

roles_router = Blueprint("roles", __name__)


@roles_router.route(f"{API_V1_STR}/roles/", methods=["POST"])
@superuser_required
def route_roles_post():
    data = request.json
    name = data["name"]
    role = get_role_by_name(g.db_session, name)
    if role:
        raise HTTPException(400, f"The role: {name} already exists in the system")
    create_role(g.db_session, name)
    return jsonify(message=f"{name} created")


@roles_router.route(f"{API_V1_STR}/roles/", methods=["GET"])
@auth_required
def route_roles_get():
    current_user = g.current_user

    if check_if_user_is_superuser(current_user):
        return [Role(**role.__dict__).dict() for role in get_roles(g.db_session)]
    else:
        return [Role(**role.__dict__).dict() for role in get_user_roles(current_user)]
