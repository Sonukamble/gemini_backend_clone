from pydantic import BaseModel, Field
from typing import Optional


class UserResponse(BaseModel):
    """
    Response schema for a user object returned from the API.
    """
    id: str = Field(..., example="a1b2c3d4")
    mobile_number: str = Field(..., example="9876543210")
    name: Optional[str] = Field(None, example="John Doe")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "a1b2c3d4",
                "mobile_number": "9876543210",
                "name": "John Doe"
            }
        }
