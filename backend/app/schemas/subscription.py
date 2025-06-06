from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal
from decimal import Decimal

class SubscriptionBase(BaseModel):
    name: str
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    currency: str = "USD"
    billing_cycle: Literal["monthly", "yearly"]
    next_due_date: date

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(BaseModel):
    name: str | None = None
    amount: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    currency: str | None = None
    billing_cycle: Literal['monthly', 'yearly'] | None = None
    next_due_date: date | None = None

class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True