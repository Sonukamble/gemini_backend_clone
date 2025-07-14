from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status
from starlette.responses import JSONResponse
from typing import List


from db.session import get_db
from schemas.chatroom import ChatroomCreate, ChatroomRead
from services import chatroom_service
from core import caching
from models.user import User
from core.auth_utils import get_current_user
from core.logger import logger

chat_router = APIRouter(prefix="/chat", tags=["Chat"])

@chat_router.post("/chatroom", response_model=ChatroomRead, status_code=status.HTTP_201_CREATED)
async def create_chatroom(
    chatroom: ChatroomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new chatroom for the current authenticated user.
    """
    try:
        new_room = chatroom_service.create_chatroom(db, current_user.id, chatroom)
        chatroom_response = ChatroomRead.model_validate(new_room)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Chatroom created successfully",
                "chatroom": chatroom_response.model_dump(mode="json")
            }
        )
    except Exception as e:
        logger.error(f"Chatroom creation failed for user {current_user.id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create chatroom")


@chat_router.get("/chatroom", response_model=list[ChatroomRead])
async def get_chatrooms(db: Session = Depends(get_db), current_user: User = Depends(get_current_user))-> List[ChatroomRead]:
    """
    Retrieve all chatrooms for the current authenticated user.
    """
    try:
        # Check if chatrooms are cached
        cached = await caching.get_cached_chatrooms(current_user.id)
        if cached:
            return cached
        
        chatrooms = chatroom_service.get_chatrooms(db, current_user.id)
        result = [ChatroomRead.model_validate(c) for c in chatrooms]
        
        # Cache the chatrooms
        await caching.set_cached_chatrooms(current_user.id, [r.model_dump() for r in result])
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Chatrooms retrieved successfully",
                "chatrooms": [r.model_dump(mode="json") for r in result]
            }
        )
    except Exception as e:
        logger.error(f"Error retrieving chatrooms for user {current_user.id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve chatrooms")


@chat_router.get("/chatroom/{id}", response_model=ChatroomRead)
async def get_chatroom(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve a chatroom by ID for the current authenticated user.
    """
    try:
        chatroom = chatroom_service.get_chatroom_by_id(db, id, current_user.id)
        if not chatroom:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, detail="Chatroom not found")
        
        chatroom_response = ChatroomRead.model_validate(chatroom)
        chatroom_data = chatroom_response.model_dump(mode="json")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Chatroom retrieved successfully",
                "chatroom": chatroom_data
            }
        )
    except HTTPException as e:
        logger.error(f"Chatroom retrieval failed for user {current_user.id}: {e.detail}")
        raise e 
    except Exception as e:
        logger.error(f"Unexpected error retrieving chatroom {id} for user {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
