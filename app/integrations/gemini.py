# app/services/gemini_client.py

import google.generativeai as genai
from typing import List, Dict

from app.config import Config
from app.core.logger import logger

MAX_TOTAL_TOKENS = 8192
MAX_OUTPUT_TOKENS = 1024
MAX_INPUT_TOKENS = MAX_TOTAL_TOKENS - MAX_OUTPUT_TOKENS
SAFE_INPUT_TOKENS = 7000

class GeminiChatClient:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.api_key = Config.GOOGLE_API_KEY
        self.model_name = model_name
        self._configure_client()
        self._initialize_model()

    def _configure_client(self):
        genai.configure(api_key=self.api_key)

    def _initialize_model(self):
        self.generation_config = {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config
        )

    def count_prompt_tokens(self, full_history):
        try:
            return self.model.count_tokens(full_history)
        except Exception as e:
            logger.error(f"Error counting tokens: {e}")
            return None

    def get_response(
        self,
        chat_history: List[Dict[str, List[str]]],
        question: str,
        model_prompt: str
    ) -> str:
        full_history = [{"role": "model", "parts": [model_prompt]}] + chat_history

        try:
            while True:
                token_count = self.count_prompt_tokens(full_history)
                if token_count and token_count.total_tokens < SAFE_INPUT_TOKENS:
                    break

                if len(full_history) <= 2:
                    return (
                        "Your chat history is too long to continue.\n"
                        "Please create a new chatroom to start fresh."
                    )

                removed = full_history.pop(1)
                logger.info(f"Dropped message to reduce tokens: {removed}")
        except Exception as e:
            logger.error(f"Token trimming failed: {e}")

        # Proceed with Gemini call
        try:
            chat_session = self.model.start_chat(history=full_history)
            response = chat_session.send_message(question)
            return response.text
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {e}")
            return "Error getting response from Gemini. Please try again."
