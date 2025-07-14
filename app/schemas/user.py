from pydantic import BaseModel, Field
from typing import Optional


class UserResponse(BaseModel):
    """
    Response schema for a user object returned from the API.
    """
    id: str = Field(..., example="a1b2c3d4")
    mobile_number: str = Field(..., example="9876543210")
    name: Optional[str] = Field(None, example="John Doe")

    model_config = {
        "from_attributes": True
    }