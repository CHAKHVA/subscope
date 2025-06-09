from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD", nullable=False)
    billing_cycle = Column(String, nullable=False)
    next_due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now(datetime.UTC))
    updated_at = Column(
        DateTime,
        default=datetime.now(datetime.UTC),
        onupdate=datetime.now(datetime.UTC),
    )

    __table_args__ = (
        CheckConstraint(
            "billing_cycle IN ('monthly', 'yearly')", name="check_billing_cycle"
        ),
    )

    user = relationship("User", back_populates="subscriptions")
    reminders = relationship(
        "Reminder", back_populates="subscription", cascade="all, delete-orphan"
    )
    subscription_tags = relationship(
        "SubscriptionTag", back_populates="subscription", cascade="all, delete-orphan"
    )
