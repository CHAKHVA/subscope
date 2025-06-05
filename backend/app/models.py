from datetime import datetime
from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey, Numeric, CheckConstraint, Date, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    currency = Column(String, default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Subscriptions(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        CheckConstraint("billing_cycle IN ('monthly', 'yearly')", name='check_billing_cycle'),
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Numeric(10, 2))
    currency = Column(String, default="USD")
    billing_cycle = Column(String)
    next_due_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Tags(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='unique_user_tag'),
    )
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)

class SubscriptionTags(Base):
    __tablename__ = "subscription_tags"
    
    subscription_id = Column(Integer, ForeignKey('subscriptions.id',ondelete='CASCADE'), primary_key=True,)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

class Reminders(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    subscription_id = Column(Integer, ForeignKey('subscriptions.id', ondelete='CASCADE'), nullable=False)
    remind_at = Column(DateTime(timezone=True), nullable=False)
    is_recurring = Column(Boolean, default=True)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class NotificationLogs(Base):
    __tablename__ = "notification_logs"
    __table_args__ = (
        CheckConstraint("channel IN ('email')", name='check_channel'),
        CheckConstraint("status IN ('sent', 'failed')", name='check_status'),
    )
    
    id = Column(Integer, primary_key=True)
    reminder_id = Column(Integer, ForeignKey('reminders.id', ondelete='CASCADE'), nullable=False)
    channel = Column(String)
    status = Column(String)
    message = Column(String)
    error = Column(String)
    sent_at = Column(DateTime(timezone=True))