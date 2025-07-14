from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class MessageCreate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: int
    sender: Literal["user", "gemini"]
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
