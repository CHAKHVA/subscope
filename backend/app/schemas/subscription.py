from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Tag, field_validator


class SubscriptionBase(BaseModel):
    name: str
    amount: Decimal
    currency: str = "USD"
    billing_cycle: str
    next_due_date: date

    @field_validator("billing_cycle")
    def validate_billing_cycle(cls, v: str) -> str:
        if v not in ["monthly", "yearly"]:
            raise ValueError("billing_cycle must be either monthly or yearly")
        return v


class SubscriptionCreate(SubscriptionBase):
    tag_ids: list[int] | None = []


class SubscriptionUpdate(BaseModel):
    name: str | None = None
    amount: Decimal | None = None
    currency: str | None = None
    billing_cycle: str | None = None
    next_due_date: date | None = None
    tag_ids: list[int] = []

    @field_validator("billing_cycle")
    def validate_billing_cycle(cls, v: str) -> str:
        if v not in ["monthly", "yearly"]:
            raise ValueError("billing_cycle must be either monthly or yearly")
        return v


class SubscriptionInDB(SubscriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Subscription(SubscriptionInDB):
    tags: list[Tag] = []
