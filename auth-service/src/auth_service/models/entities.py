from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Date, UUID, Integer, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class Base(DeclarativeBase):
    pass

class UserCredits(Base):
    __tablename__ = "users_credits"
    id = Column(UUID, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now())
    role_id = Column(Integer, ForeignKey("users_roles.id"), nullable=False, default=0)

    role = relationship("Role", back_populates="users", lazy="select")


class Role(Base):
    __tablename__ = "users_roles"
    id = Column(Integer, nullable=False, primary_key=True)
    role = Column(String, nullable=False)

    users = relationship("UserCredits", back_populates="role", lazy="select")
