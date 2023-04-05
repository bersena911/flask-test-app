import re
from datetime import datetime, timedelta
from functools import wraps

import jwt
from jwt import ExpiredSignatureError, PyJWTError
from flask import request, g

from core.errors import HTTPException
from settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"


def decode_jwt(token):
    """
    Gets information from jwt token
    Args:
        token: JWT token

    Returns:
        (dict): decoded information
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def validate_token_format(token):
    """
    Validates JWT token format.

    Args:
        token (str): User provided token

    Returns:
        str or None: Validated and extracted token or None
    """
    token = re.sub(r"\s+", " ", token)
    token_parts = token.split()
    if (
        token_parts
        and len(token_parts) == 2
        and token_parts[0].lower() in ("bearer", "token")
    ):
        return token_parts[1]
    return None


def create_access_token(
    data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    """
    Creates access token using python-jose library
    Args:
        data: data to encode inside token
        expire_minutes: optional token expiration time. defaults to 30

    Returns:
        str: created access token

    """
    to_encode = data.copy()
    to_encode["id"] = str(to_encode["id"])
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def auth_required(f):
    """
    Checks if the user is authenticated via cognito
    Args:
        f: Function to be decorated

    Returns:

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise HTTPException(400, "Authorization Header Not Provided")

        token = validate_token_format(authorization_header)
        if not token:
            raise HTTPException(401, "Authorization Header Not Provided")
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(400, "Access Token Has Expired")
        except PyJWTError:
            raise HTTPException(500, "Invalid Token")

        g.id_token = decoded_token
        g.access_token = token
        g.current_user = decoded_token
        return f(*args, **kwargs)

    return decorated_function
