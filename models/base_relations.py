from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("user.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)
