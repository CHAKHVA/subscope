from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class SubscriptionTag(Base):
    __tablename__ = "subscription_tags"

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    subscription = relationship("Subscription", back_populates="subscription_tags")
    tag = relationship("Tag", back_populates="subscription_tags")
