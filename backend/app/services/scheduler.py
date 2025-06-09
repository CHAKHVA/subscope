from datetime import datetime, timedelta
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.notification_log import notification_log as crud_notification_log
from app.crud.reminder import reminder as crud_reminder
from app.schemas.reminder import NotificationLogCreate
from app.services.email import send_reminder_email

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start(self):
        """Start the scheduler."""
        self.scheduler.add_job(
            self.check_reminders,
            IntervalTrigger(minutes=5),
            id="reminder_checker",
            max_instances=1,
        )
        self.scheduler.start()
        logger.info("Scheduler started")

    async def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")

    async def check_reminders(self):
        """Check and send reminder emails."""
        logger.info("Checking for reminders to send...")

        db: Session = SessionLocal()
        try:
            # Get reminders that need to be sent
            now = datetime.utcnow()
            upcoming = now + timedelta(hours=1)

            reminders = crud_reminder.get_pending_reminders(
                db=db, from_time=now, to_time=upcoming
            )

            logger.info(f"Found {len(reminders)} reminders to process")

            for reminder in reminders:
                try:
                    subscription = reminder.subscription
                    user = subscription.user

                    # Send reminder email
                    success = send_reminder_email(
                        email=user.email,
                        full_name=user.full_name or "User",
                        subscription_name=subscription.name,
                        amount=f"{subscription.currency} {subscription.amount}",
                        due_date=subscription.next_due_date.strftime("%Y-%m-%d"),
                    )

                    # Log the attempt
                    log_data = NotificationLogCreate(
                        reminder_id=reminder.id,
                        channel="email",
                        status="sent" if success else "failed",
                        message=f"Reminder for {subscription.name}",
                        error=None if success else "Failed to send email",
                    )
                    crud_notification_log.create(db=db, obj_in=log_data)

                    # Mark reminder as sent if successful
                    if success:
                        reminder.sent = "true"
                        db.add(reminder)
                        logger.info(
                            f"Sent reminder for {subscription.name} to {user.email}"
                        )
                    else:
                        logger.error(
                            f"Failed to send reminder for {subscription.name} to {user.email}"
                        )

                except Exception as e:
                    logger.error(f"Error processing reminder {reminder.id}: {e!s}")

            db.commit()

        except Exception as e:
            logger.error(f"Error in check_reminders: {e!s}")
            db.rollback()
        finally:
            db.close()


scheduler_service = SchedulerService()
