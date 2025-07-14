from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ChatroomBase(BaseModel):
    title: str

class ChatroomCreate(ChatroomBase):
    pass

class ChatroomRead(ChatroomBase):
    id: UUID
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

        