from flask import Blueprint, g

from core.errors import HTTPException
from core.jwt import auth_required
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
def route_users_get():
    current_user = g.current_user

    if check_if_user_is_superuser(current_user):
        return [UserDetails(**user.__dict__).dict() for user in get_users()]
    else:
        # return the current user's data, but in a list
        return [current_user]


@users_router.route(f"{API_V1_STR}/users/", methods=["POST"])
@auth_required
def route_users_post(email=None, password=None, first_name=None, last_name=None):
    current_user = g.current_user

    if not check_if_user_is_superuser(current_user):
        HTTPException(400, "Only a superuser can execute this action")

    user = get_user_by_username(email)

    if user:
        return HTTPException(
            400, f"The user with this email already exists in the system: {email}"
        )
    user = create_user(email, password, first_name, last_name)
    return UserDetails(**user.__dict__).dict()


@users_router.route(f"{API_V1_STR}/users/me", methods=["GET"])
@auth_required
def route_users_me_get():
    return g.current_user


@users_router.route(f"{API_V1_STR}/users/<int:user_id>", methods=["GET"])
@auth_required
def route_users_id_get(user_id):
    current_user = g.current_user

    if not check_if_user_is_superuser(current_user):
        return HTTPException(400, "Not authorized")

    user = get_user_by_id(user_id)

    if not user:
        return HTTPException(400, f"The user with id: {user_id} does not exists")

    return UserDetails(**user.__dict__).dict()


@users_router.route(f"{API_V1_STR}/users/<int:user_id>/roles/", methods=["POST"])
@auth_required
def route_users_assign_role_post(user_id, role_id):
    current_user = g.current_user

    if not check_if_user_is_superuser(current_user):
        HTTPException(404, "Not authorized")

    user = get_user_by_id(user_id)
    if not user:
        return HTTPException(400, f"The user with id: {user_id} does not exists")

    role = get_role_by_id(role_id)
    if not role:
        return HTTPException(400, f"The role does not exist")

    updated_user = assign_role_to_user(role, user)
    return UserDetails(**updated_user.__dict__).dict()
