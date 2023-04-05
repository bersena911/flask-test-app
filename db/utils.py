from core.security import get_password_hash
from models.role import Role
from models.user import User


def check_if_user_is_active(user):
    return user["is_active"]


def check_if_user_is_superuser(user):
    return user["is_superuser"]


def get_role_by_name(session, name):
    return session.query(Role).filter(Role.name == name).first()


def get_role_by_id(session, role_id):
    return session.query(Role).filter(Role.id == role_id).first()


def create_role(session, name):
    role = Role(name=name)
    session.add(role)
    session.commit()
    return role


def get_roles(session):
    return session.query(Role).all()


def get_user_roles(user):
    return user.roles


def get_user_by_username(session, username) -> User:
    return session.query(User).filter(User.email == username).first()


def get_user_by_id(session, user_id):
    return session.query(User).filter(User.id == user_id).first()


def get_user_hashed_password(user):
    return user.password


def get_users(session):
    return session.query(User).all()


def create_user(
    session, username, password, first_name=None, last_name=None, is_superuser=False
):
    user = User(
        email=username,
        password=get_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        is_superuser=is_superuser,
    )
    session.add(user)
    session.commit()
    return user


def assign_role_to_user(session, role: Role, user: User):
    user.roles.append(role)
    session.add(user)
    session.commit()
    return user
