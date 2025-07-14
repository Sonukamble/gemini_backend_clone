# from app.integrations.gemini import GeminiAPI
from typing import Dict, List
from db.session import SessionLocal
from integrations.gemini import GeminiChatClient
from services.message_service import create_gemini_message
from workers.queue import Celery_app
from sqlalchemy.orm import Session

from core.logger import logger

@Celery_app.task(name="workers.message_task.process_message_response")
def process_gemini_response(chatroom_id: str,chat_history: List[Dict[str, List[str]]], user_message: str):   
    """
    Process the response from Gemini API and save it as a message in the chatroom. 
    """
 
    db = SessionLocal()
    try:
  
        client = GeminiChatClient()
        logger.info(f"Processing Gemini response for chatroom {chatroom_id}")

        prompt="You are an intelligent and helpful AI assistant. Answer user questions clearly, accurately, and concisely. Provide additional context or suggestions when helpful."
        response=client.get_response(chat_history, user_message, prompt)
        create_gemini_message(db, chatroom_id, response)
    finally:
        db.close()
    
    