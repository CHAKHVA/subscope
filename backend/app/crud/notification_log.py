from datetime import datetime, timezone

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.notification_log import NotificationLogs
from app.schemas.notification_log import NotificationLogCreate, NotificationLogUpdate


class CRUDNotificationLog(
    CRUDBase[NotificationLogs, NotificationLogCreate, NotificationLogUpdate]
):
    def get_by_reminder(
        self, db: Session, *, reminder_id: int
    ) -> list[NotificationLogs]:
        """Get all notification logs for a specific reminder."""
        return (
            db.query(self.model)
            .filter(self.model.reminder_id == reminder_id)
            .order_by(self.model.sent_at.desc())
            .all()
        )

    def get_by_status(
        self, db: Session, *, status: str, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get notification logs by status (sent/failed)."""
        return (
            db.query(self.model)
            .filter(self.model.status == status)
            .order_by(self.model.sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_failed_notifications(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get all failed notification logs."""
        return self.get_by_status(db, status="failed", skip=skip, limit=limit)

    def get_sent_notifications(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get all successfully sent notification logs."""
        return self.get_by_status(db, status="sent", skip=skip, limit=limit)

    def get_by_channel(
        self, db: Session, *, channel: str, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get notification logs by channel (email)."""
        return (
            db.query(self.model)
            .filter(self.model.channel == channel)
            .order_by(self.model.sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_logs_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        status: str | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[NotificationLogs]:
        """Get notification logs within a date range."""
        query = db.query(self.model).filter(
            and_(self.model.sent_at >= start_date, self.model.sent_at <= end_date)
        )

        if status:
            query = query.filter(self.model.status == status)

        return query.order_by(self.model.sent_at.desc()).offset(skip).limit(limit).all()

    def get_recent_logs(
        self, db: Session, *, hours: int = 24, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get notification logs from the last X hours."""
        current_time = datetime.now(timezone.utc)
        start_time = current_time.replace(hour=current_time.hour - hours)

        return self.get_logs_by_date_range(
            db, start_date=start_time, end_date=current_time, skip=skip, limit=limit
        )

    def create_notification_log(
        self,
        db: Session,
        *,
        reminder_id: int,
        channel: str = "email",
        status: str = "sent",
        message: str,
        error: str | None = None,
    ) -> NotificationLogs:
        """Create a notification log entry."""
        log_data = NotificationLogCreate(
            reminder_id=reminder_id,
            channel=channel,
            status=status,
            message=message,
            error=error,
            sent_at=datetime.now(timezone.utc) if status == "sent" else None,
        )
        return self.create(db, obj_in=log_data)

    def mark_as_failed(
        self, db: Session, *, log_id: int, error_message: str
    ) -> NotificationLogs | None:
        """Mark a notification log as failed with error message."""
        log = self.get(db, id=log_id)
        if log:
            log.status = "failed"
            log.error = error_message
            log.sent_at = datetime.now(timezone.utc)
            db.add(log)
            db.commit()
            db.refresh(log)
        return log

    def get_retry_candidates(
        self, db: Session, *, max_age_hours: int = 24
    ) -> list[NotificationLogs]:
        """Get failed notifications that might be candidates for retry."""
        cutoff_time = datetime.now(timezone.utc).replace(
            hour=datetime.now(timezone.utc).hour - max_age_hours
        )

        return (
            db.query(self.model)
            .filter(
                and_(self.model.status == "failed", self.model.sent_at >= cutoff_time)
            )
            .order_by(self.model.sent_at.desc())
            .all()
        )

    def get_logs_with_errors(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[NotificationLogs]:
        """Get notification logs that have error messages."""
        return (
            db.query(self.model)
            .filter(self.model.error.isnot(None))
            .order_by(self.model.sent_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_status(self, db: Session, *, status: str) -> int:
        """Count notification logs by status."""
        return db.query(self.model).filter(self.model.status == status).count()

    def get_notification_stats(self, db: Session) -> dict[str, int | float]:
        """Get basic statistics about notifications."""
        total = db.query(self.model).count()
        sent = self.count_by_status(db, status="sent")
        failed = self.count_by_status(db, status="failed")

        return {
            "total": total,
            "sent": sent,
            "failed": failed,
            "success_rate": (sent / total * 100) if total > 0 else 0,
        }

    def delete_by_reminder(self, db: Session, *, reminder_id: int) -> int:
        """Delete all notification logs for a specific reminder."""
        deleted_count = (
            db.query(self.model).filter(self.model.reminder_id == reminder_id).delete()
        )
        db.commit()
        return deleted_count


# Create an instance of the CRUD class
notification_log = CRUDNotificationLog(NotificationLogs)
