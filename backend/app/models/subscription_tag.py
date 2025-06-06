from sqlalchemy import Column, ForeignKey, Integer

from app.core.database import Base


class SubscriptionTags(Base):
    __tablename__ = "subscription_tags"

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
