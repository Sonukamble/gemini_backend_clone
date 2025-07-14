from fastapi import HTTPException
from models.chatroom import Chatroom
from schemas.chatroom import ChatroomCreate
from core.logger import logger
import uuid

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

def create_chatroom(db: Session, user_id: str, chatroom: ChatroomCreate) -> Chatroom:
    """
    Create a new chatroom for a user.
    """
    try:
        db_chatroom = Chatroom(id=str(uuid.uuid4()),user_id=user_id, title=chatroom.title)
        db.add(db_chatroom)
        db.commit()
        db.refresh(db_chatroom)
        logger.info(f"Chatroom created: {db_chatroom.id} by user: {user_id}")
        return db_chatroom
    except Exception as e:
        logger.error(f"Error creating chatroom for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create chatroom"
        )

def get_chatrooms(db: Session, user_id: int):
    """ Retrieve all chatrooms for a user.
    """
    try:
        chatrooms = db.query(Chatroom).filter(Chatroom.user_id == user_id).all()
        logger.info(f"Retrieved {len(chatrooms)} chatrooms for user {user_id}")
        return chatrooms
    except Exception as e:
        logger.error(f"Error retrieving chatrooms for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chatrooms")

def get_chatroom_by_id(db: Session, chatroom_id: int, user_id: int):
    """
    Retrieve a chatroom by ID that belongs to a specific user.
    """
    try:
        chatroom = db.query(Chatroom).filter(Chatroom.id == chatroom_id, Chatroom.user_id == user_id).first()
    
        if not chatroom:
            logger.warning(f"Chatroom {chatroom_id} not found for user {user_id}")
        else:
            logger.info(f"Chatroom {chatroom_id} retrieved for user {user_id}")

        return chatroom
    except Exception as e:
        logger.error(f"Error retrieving chatroom {chatroom_id} for user {user_id}: {e}")
        raise HTTPException(status_code=404, detail="Chatroom not found")
    