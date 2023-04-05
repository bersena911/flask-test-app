from sqlalchemy.orm import sessionmaker

from core.security import get_password_hash
from db.db_service import db_service
from models.role import Role
from models.user import User


def check_if_user_is_active(user):
    return user["is_active"]


def check_if_user_is_superuser(user):
    return user["is_superuser"]


def get_role_by_name(name):
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(Role).filter(Role.name == name).first()


def get_role_by_id(role_id):
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(Role).filter(Role.id == role_id).first()


def create_role(name):
    with sessionmaker(bind=db_service.engine)() as session:
        role = Role(name=name)
        session.add(role)
        session.commit()
        return role


def get_roles():
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(Role).all()


def get_user_roles(user):
    return user.roles


def get_user_by_username(username) -> User:
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(User).filter(User.email == username).first()


def get_user_by_id(user_id):
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(User).filter(User.id == user_id).first()


def get_user_hashed_password(user):
    return user.password


def get_user_id(user):
    return user.id


def get_users():
    with sessionmaker(bind=db_service.engine)() as session:
        return session.query(User).all()


def create_user(
    username, password, first_name=None, last_name=None, is_superuser=False, role=None
):
    with sessionmaker(bind=db_service.engine)() as session:
        user = User(
            email=username,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
        )
        if role:
            user.roles.append(role)
        session.add(user)
        session.commit()
        return user


def assign_role_to_user(role: Role, user: User):
    with sessionmaker(bind=db_service.engine)() as session:
        user.roles.append(role)
        session.add(user)
        session.commit()
        return user
