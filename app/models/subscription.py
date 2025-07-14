from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
import datetime
import enum as py_enum

from app.db.base import Base

class SubscriptionTierEnum(str, py_enum.Enum):
    basic = "basic"
    pro = "pro"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"),nullable=False)
    tier = Column(Enum(SubscriptionTierEnum, name="subscription_tier_enum"), nullable=False, default=SubscriptionTierEnum.basic)
    start_date = Column(DateTime, server_default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=True)

