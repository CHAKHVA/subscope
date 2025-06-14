from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class NotificationLogBase(BaseModel):
    reminder_id: int
    channel: Literal["email"]
    status: Literal["sent", "failed"]
    message: str | None = None
    error: str | None = None


class NotificationLogCreate(NotificationLogBase):
    pass


class NotificationLogResponse(NotificationLogBase):
    id: int
    sent_at: datetime

    class Config:
        from_attributes = True
