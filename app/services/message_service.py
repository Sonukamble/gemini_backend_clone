from fastapi import HTTPException
from models.message import Message, SenderEnum
from core.logger import logger

from sqlalchemy.orm import Session

def create_user_message(db: Session, chatroom_id: int, content: str):
    """
    Create a message sent by the user in a chatroom.
    """
    try:
        msg = Message(chatroom_id=chatroom_id, sender=SenderEnum.user, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        logger.info(f"Message created: {msg.id} by user: {chatroom_id}")
        return msg
        
    except Exception as e:
        logger.error(f"Error creating message for user {chatroom_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create message"
        )
    

def create_gemini_message(db: Session, chatroom_id: int, content: str):
    """
    Create a message sent by Gemini in a chatroom.
    """
    try:
        msg = Message(chatroom_id=chatroom_id, sender=SenderEnum.gemini, content=content)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        logger.info(f"Gemini message created: {msg.id} in chatroom: {chatroom_id}")
        return msg
    except Exception as e:
        logger.error(f"Error creating Gemini message for chatroom {chatroom_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create Gemini message"
        )

def get_messages(db: Session, chatroom_id: int):
    """
    Retrieve all messages in a chatroom.
    """
    try:
        messages = db.query(Message).filter(Message.chatroom_id == chatroom_id).order_by(Message.created_at).all()
        logger.info(f"Retrieved {len(messages)} messages for chatroom {chatroom_id}")
        return messages
    except Exception as e:
        logger.error(f"Error retrieving messages for chatroom {chatroom_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")
    
    

def get_chat_history(db: Session, chatroom_id: str):
    """
    Fetch all messages for a given chatroom, ordered by creation time.
    """
    try:
        messages = db.query(Message).filter(Message.chatroom_id == chatroom_id).order_by(Message.created_at).all()
        logger.info(f"Chat history retrieved for chatroom {chatroom_id} with {len(messages)} messages")
        return messages
    except Exception as e:
        logger.error(f"Error retrieving chat history for chatroom {chatroom_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")
