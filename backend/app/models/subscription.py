from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.sql import func

from app.core.database import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint(
            "billing_cycle IN ('monthly', 'yearly')", name="check_billing_cycle"
        ),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(String, nullable=False)
    amount = Column(Numeric(10, 2))
    currency = Column(String, default="USD")
    billing_cycle = Column(String)
    next_due_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
