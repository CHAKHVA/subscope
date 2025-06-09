from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "name", name="unique_user_tag"),)

    user = relationship("User", back_populates="tags")
    subscription_tags = relationship(
        "SubscriptionTag", back_populates="tag", cascade="all, delete-orphan"
    )
