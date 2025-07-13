from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from db.base import Base
from sqlalchemy.orm import relationship

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    chatroom_id = Column(String, ForeignKey("chatrooms.id"), nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'gemini'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chatroom = relationship("Chatroom", back_populates="messages")
