from sqlalchemy.orm import sessionmaker

from db.db_service import db_service
from db.utils import (
    get_role_by_name,
    create_role,
    get_user_by_username,
    create_user,
    assign_role_to_user,
)
from settings import get_config

config = get_config()


def init_db():
    db_service.create_engine()
    with sessionmaker(bind=db_service.engine)() as session:
        role = get_role_by_name(session, "default")
        if not role:
            role = create_role(session, "default")

        user = get_user_by_username(session, config.get("FIRST_SUPERUSER"))
        if not user:
            user = create_user(
                session,
                config.get("FIRST_SUPERUSER"),
                config.get("FIRST_SUPERUSER_PASSWORD"),
                is_superuser=True,
            )
            assign_role_to_user(session, role, user)
