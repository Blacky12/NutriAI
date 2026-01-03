from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base


class SubscriptionTier(enum.Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    subscription = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False)
    daily_quota = Column(Integer, default=10, nullable=False)
    quota_used = Column(Integer, default=0, nullable=False)
    quota_reset_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")

    def has_reached_quota(self) -> bool:
        return self.daily_quota != -1 and self.quota_used >= self.daily_quota

