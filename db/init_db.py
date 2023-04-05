from db.db_service import db_service
from db.utils import (
    get_role_by_name,
    create_role,
    get_user_by_username,
    create_user,
)
from settings import get_config

config = get_config()


def init_db():
    db_service.create_engine()
    role = get_role_by_name("default")
    if not role:
        role = create_role("default")

    user = get_user_by_username(config.get("FIRST_SUPERUSER"))
    if not user:
        create_user(
            config.get("FIRST_SUPERUSER"),
            config.get("FIRST_SUPERUSER_PASSWORD"),
            is_superuser=True,
            role=role,
        )
