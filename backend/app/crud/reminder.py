from datetime import datetime, timezone

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate


class CRUDReminder(CRUDBase[Reminder, ReminderCreate, ReminderUpdate]):
    def get_by_subscription(
        self, db: Session, *, subscription_id: int
    ) -> list[Reminder]:
        """Get all reminders for a specific subscription."""
        return (
            db.query(self.model)
            .filter(self.model.subscription_id == subscription_id)
            .all()
        )

    def get_pending_reminders(
        self, db: Session, *, current_time: datetime | None = None
    ) -> list[Reminder]:
        """Get all pending reminders (not sent and due before current time)."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        return (
            db.query(self.model)
            .filter(and_(not self.model.is_sent, self.model.remind_at <= current_time))
            .all()
        )

    def get_sent_reminders(
        self, db: Session, *, subscription_id: int | None = None
    ) -> list[Reminder]:
        """Get all sent reminders, optionally filtered by subscription."""
        query = db.query(self.model).filter(self.model.is_sent)

        if subscription_id:
            query = query.filter(self.model.subscription_id == subscription_id)

        return query.all()

    def get_recurring_reminders(
        self, db: Session, *, subscription_id: int | None = None
    ) -> list[Reminder]:
        """Get all recurring reminders, optionally filtered by subscription."""
        query = db.query(self.model).filter(self.model.is_recurring)

        if subscription_id:
            query = query.filter(self.model.subscription_id == subscription_id)

        return query.all()

    def mark_as_sent(self, db: Session, *, reminder_id: int) -> Reminder | None:
        """Mark a reminder as sent."""
        reminder = self.get(db, id=reminder_id)
        if reminder:
            reminder.is_sent = True
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
        return reminder

    def mark_multiple_as_sent(
        self, db: Session, *, reminder_ids: list[int]
    ) -> list[Reminder]:
        """Mark multiple reminders as sent."""
        reminders = db.query(self.model).filter(self.model.id.in_(reminder_ids)).all()

        for reminder in reminders:
            reminder.is_sent = True
            db.add(reminder)

        db.commit()

        for reminder in reminders:
            db.refresh(reminder)

        return reminders

    def get_reminders_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        subscription_id: int | None = None,
        include_sent: bool = True,
    ) -> list[Reminder]:
        """Get reminders within a date range."""
        query = db.query(self.model).filter(
            and_(self.model.remind_at >= start_date, self.model.remind_at <= end_date)
        )

        if subscription_id:
            query = query.filter(self.model.subscription_id == subscription_id)

        if not include_sent:
            query = query.filter(not self.model.is_sent)

        return query.all()

    def get_overdue_reminders(
        self, db: Session, *, current_time: datetime | None = None
    ) -> list[Reminder]:
        """Get overdue reminders (not sent and past due date)."""
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        return (
            db.query(self.model)
            .filter(and_(not self.model.is_sent, self.model.remind_at < current_time))
            .all()
        )

    def reset_sent_status(self, db: Session, *, reminder_id: int) -> Reminder | None:
        """Reset the sent status of a reminder (mark as not sent)."""
        reminder = self.get(db, id=reminder_id)
        if reminder:
            reminder.is_sent = False
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
        return reminder

    def update_remind_time(
        self, db: Session, *, reminder_id: int, new_remind_at: datetime
    ) -> Reminder | None:
        """Update the remind_at time for a specific reminder."""
        reminder = self.get(db, id=reminder_id)
        if reminder:
            reminder.remind_at = new_remind_at
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
        return reminder

    def delete_by_subscription(self, db: Session, *, subscription_id: int) -> int:
        """Delete all reminders for a specific subscription."""
        deleted_count = (
            db.query(self.model)
            .filter(self.model.subscription_id == subscription_id)
            .delete()
        )
        db.commit()
        return deleted_count


# Create an instance of the CRUD class
reminder = CRUDReminder(Reminder)
