from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class SenderEnum(str, enum.Enum):
    user = "user"
    gemini = "gemini"

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chatroom_id = Column(String, ForeignKey("chatrooms.id"),nullable=False)
    sender = Column(Enum(SenderEnum), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Chatroom(id={self.id}, title={self.title}, user_id={self.user_id})>"