from pydantic import BaseModel

class SubscriptionStatusResponse(BaseModel):
    tier: str
