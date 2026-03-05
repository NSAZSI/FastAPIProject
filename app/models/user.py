from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from app.db.base_class import Base


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)