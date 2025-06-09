from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    currency = Column(String, default="USD", nullable=False)
    created_at = Column(DateTime, default=datetime.now(datetime.UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(datetime.UTC),
        onupdate=datetime.now(datetime.UTC),
    )

    subscriptions = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
    )
    tags = relationship("Tags", back_populates="user", cascade="all, delete-orphan")
