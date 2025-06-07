from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String

from app.core.database import Base


class NotificationLogs(Base):
    __tablename__ = "notification_logs"
    __table_args__ = (
        CheckConstraint("channel IN ('email')", name="check_channel"),
        CheckConstraint("status IN ('sent', 'failed')", name="check_status"),
    )

    id = Column(Integer, primary_key=True)
    reminder_id = Column(
        Integer, ForeignKey("reminders.id", ondelete="CASCADE"), nullable=False
    )
    channel = Column(String)
    status = Column(String)
    message = Column(String)
    error = Column(String)
    sent_at = Column(DateTime(timezone=True))
