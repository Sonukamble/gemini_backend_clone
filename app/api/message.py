from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from services.limiting import check_prompt_limit
from services.subscription_service import SubscriptionService
from schemas.message import MessageCreate, MessageRead
from services import message_service
from workers.message_task import process_gemini_response
from models.user import User
from core.logger import logger
from core.auth_utils import get_current_user

from starlette.responses import JSONResponse

message_router = APIRouter(prefix="/message", tags=["Message"])

@message_router.post("/{chatroom_id}", response_model=list[MessageRead], status_code=201)
async def send_message(chatroom_id: str, msg: MessageCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """
    Send a message in a chatroom.
    This will create a user message and trigger the Gemini response
    """
    try:
        # check the status of the user's subscription
        subscription =await SubscriptionService.get_status(user_id=current_user.id)
        if subscription.status_code==404:
            logger.error(f"Subscription not found for user {current_user.id}")
            # tier = subscription.tier.value if subscription else "basic"

            # Enforce usage limit
            await check_prompt_limit(current_user.id, 'basic')

        # Create user message
        user_msg = message_service.create_user_message(db, chatroom_id, msg.content)

        # Fetch chat history and chatroom context
        chat_history_raw = message_service.get_chat_history(db, chatroom_id)
        chat_history = [
            {"role": msg.sender.value, "parts": [msg.content]}
            for msg in chat_history_raw
        ]

        process_gemini_response.delay(
            chat_history=chat_history,
            user_message=msg.content,
            chatroom_id=chatroom_id,
        )
        
        
        user_message={
            "id": user_msg.id,
            "chatroom_id": user_msg.chatroom_id,
            "sender": user_msg.sender.value,
            "content": user_msg.content,
            "created_at": user_msg.created_at.isoformat()
        }

        return JSONResponse(
            status_code=201,
            content={
                "message": "Message sent successfully",
                "data": user_message
            }
        )
    
    except Exception as e:
        logger.error(f"Error sending message in chatroom {chatroom_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")
    

@message_router.get("/{chatroom_id}", response_model=list[MessageRead], status_code=200)
async def get_chatroom_messages(chatroom_id: str, db: Session = Depends(get_db),
                                current_user: User = Depends(get_current_user)):
    """
    Retrieve all messages in a chatroom.
    """
    try:
        messages = message_service.get_messages(db, chatroom_id)
        return messages
    except Exception as e:
        logger.error(f"Error retrieving messages for chatroom {chatroom_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve messages")