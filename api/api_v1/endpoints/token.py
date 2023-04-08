from flask import Blueprint
from sqlalchemy.orm import sessionmaker

from core.errors import HTTPException
from core.jwt import create_access_token
from core.security import verify_password
from core.validation import validate_post_data
from db.db_service import db_service
from db.utils import get_user_by_username, get_user_hashed_password
from schemas.token import LoginData
from schemas.user import UserDetails
from settings import API_V1_STR

token_router = Blueprint("tokens", __name__)


@token_router.route(f"{API_V1_STR}/login/", methods=["POST"])
@validate_post_data
def login_access_token(data: LoginData):
    with sessionmaker(bind=db_service.engine)() as session:
        user = get_user_by_username(session, data.username)

        if not user or not verify_password(
            data.password, get_user_hashed_password(user)
        ):
            raise HTTPException(400, "Incorrect email or password")
        elif not user.is_active:
            raise HTTPException(400, "Inactive user")
        user_details = UserDetails(**user.__dict__).dict()
    return {
        "access_token": create_access_token({"sub": user.email, **user_details}, 30),
        "token_type": "bearer",
    }
