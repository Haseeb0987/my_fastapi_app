from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(5), primary_key=True, index=True)  # HH425
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
