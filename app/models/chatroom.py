from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base

class Chatroom(Base):
    __tablename__ = "chatrooms"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # user = relationship("User", back_populates="chatrooms")
    # messages = relationship("Message", back_populates="chatroom", cascade="all, delete")