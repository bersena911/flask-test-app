from flask import Blueprint, request

from core.errors import HTTPException
from core.jwt import create_access_token
from core.security import verify_password
from db.utils import get_user_by_username, get_user_hashed_password
from schemas.user import UserDetails
from settings import API_V1_STR

token_router = Blueprint("tokens", __name__)


@token_router.route(f"{API_V1_STR}/login/", methods=["POST"])
def login_access_token():
    data = request.json
    user = get_user_by_username(data["username"])

    if not user or not verify_password(
        data["password"], get_user_hashed_password(user)
    ):
        raise HTTPException(400, "Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(400, "Inactive user")
    user_details = UserDetails(**user.__dict__).dict()
    return {
        "access_token": create_access_token({"sub": user.email, **user_details}, 30),
        "token_type": "bearer",
    }
