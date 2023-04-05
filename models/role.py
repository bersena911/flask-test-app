from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from models.base_relations import users_roles


class Role(Base):
    # Own properties
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow(), index=True)
    name = Column(String, index=True)
    # Relationships
    users = relationship("User", secondary=users_roles, back_populates="roles")
