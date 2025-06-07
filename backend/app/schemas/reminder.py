from datetime import datetime

from pydantic import BaseModel


class ReminderBase(BaseModel):
    remind_at: datetime
    is_recurring: bool = True


class ReminderCreate(ReminderBase):
    subscription_id: int


class ReminderUpdate(BaseModel):
    remind_at: datetime | None = None
    is_recurring: bool | None = None
    sent: bool | None = None


class ReminderResponse(ReminderBase):
    id: int
    subscription_id: int
    sent: bool
    created_at: datetime

    class Config:
        orm_mode = True
