from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from db.base import Base
from sqlalchemy.orm import relationship

class Chatroom(Base):
    __tablename__ = "chatrooms"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship("Message", back_populates="chatroom")