from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(
        Integer, ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False
    )
    remind_at = Column(DateTime, nullable=False)
    is_recurring = Column(Boolean, default=True)
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(datetime.UTC))

    subscription = relationship("Subscription", back_populates="reminders")
    notification_logs = relationship(
        "NotificationLog", back_populates="reminder", cascade="all, delete-orphan"
    )
