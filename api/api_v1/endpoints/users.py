from flask import Blueprint, g, request, jsonify

from core.errors import HTTPException
from core.jwt import auth_required, superuser_required
from core.validation import validate_post_data
from db.utils import (
    check_if_user_is_superuser,
    get_users,
    get_user_by_username,
    create_user,
    get_user_by_id,
    get_role_by_id,
    assign_role_to_user,
)
from schemas.user import UserDetails
from settings import API_V1_STR

users_router = Blueprint("users", __name__)


@users_router.route(f"{API_V1_STR}/users/", methods=["GET"])
@auth_required
def users_get():
    current_user = g.current_user

    if check_if_user_is_superuser(current_user):
        return [UserDetails(**user.__dict__).dict() for user in get_users(g.db_session)]
    else:
        return [current_user]


@users_router.route(f"{API_V1_STR}/users/", methods=["POST"])
@superuser_required
def users_post():
    data = request.json
    email, password, first_name, last_name = (
        data["email"],
        data["password"],
        data["first_name"],
        data["last_name"],
    )
    user = get_user_by_username(g.db_session, email)

    if user:
        raise HTTPException(
            400, f"The user with this email already exists in the system: {email}"
        )
    user = create_user(g.db_session, email, password, first_name, last_name)
    return UserDetails(**user.__dict__).dict()


@users_router.route(f"{API_V1_STR}/users/me", methods=["GET"])
@auth_required
def users_me_get():
    return g.current_user


@users_router.route(f"{API_V1_STR}/users/<user_id>", methods=["GET"])
@superuser_required
def users_id_get(user_id):
    user = get_user_by_id(g.db_session, user_id)

    if not user:
        raise HTTPException(400, f"The user with id: {user_id} does not exists")

    return UserDetails(**user.__dict__).dict()


@users_router.route(f"{API_V1_STR}/users/<user_id>/roles/", methods=["POST"])
@superuser_required
@validate_post_data
def users_assign_role_post(user_id, data=dict):
    data = request.json
    role_id = data["role_id"]
    user = get_user_by_id(g.db_session, user_id)
    if not user:
        raise HTTPException(400, f"The user with id: {user_id} does not exists")

    role = get_role_by_id(g.db_session, role_id)
    if not role:
        raise HTTPException(400, f"The role does not exist")

    updated_user = assign_role_to_user(g.db_session, role, user)
    return jsonify(message=f"User {user_id} assigned a role {role_id}"), 200
