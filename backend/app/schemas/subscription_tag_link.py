from pydantic import BaseModel


class SubscriptionTagLink(BaseModel):
    subscription_id: int
    tag_id: int
