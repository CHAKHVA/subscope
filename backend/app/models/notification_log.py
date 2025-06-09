from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reminder_id = Column(
        Integer, ForeignKey("reminders.id", ondelete="CASCADE"), nullable=False
    )
    channel = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(String, nullable=True)
    error = Column(String, nullable=True)
    sent_at = Column(DateTime, default=datetime.now(datetime.UTC))

    __table_args__ = (
        CheckConstraint("channel IN ('email')", name="check_channel"),
        CheckConstraint("status IN ('sent', 'failed')", name="check_status"),
    )

    reminder = relationship("Reminder", back_populates="notification_logs")
