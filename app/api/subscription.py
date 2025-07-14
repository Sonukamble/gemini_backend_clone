from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse
from fastapi import status
from fastapi import HTTPException

from app.services.subscription_service import SubscriptionService
from app.schemas.subscription import SubscriptionStatusResponse
from app.core.logger import logger
from app.core.auth_utils import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/subscribe/pro")
async def subscribe_pro(request: Request):
    """
    Endpoint to create a Pro subscription for a user.
    """
    try:
        checkout_url = await SubscriptionService.create_pro_subscription(user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Pro subscription checkout session created successfully",
                "checkout_url": checkout_url
            }
        )
    except Exception as e:
        logger.error(f"Error creating Pro subscription for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initiate Pro subscription"
        )
    

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Endpoint to handle Stripe webhook events.
    This will verify the webhook signature and process the event."""
    try:
        # Read the raw body of the request
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")
        
        # Handle the webhook event
        response = await SubscriptionService.handle_webhook(payload, sig_header)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Webhook processed successfully"}
        )
    
    except ValueError as e:
        logger.error(f"Webhook verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature"
        )
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )
  

@router.get("/subscription/status", response_model=SubscriptionStatusResponse)
async def subscription_status(user: User = Depends(get_current_user)):
    """Endpoint to get the current subscription status of a user.
    This will return the subscription tier and status.  
    """
    try:
        # Call the service to get the subscription status
        return await SubscriptionService.get_status(user_id=user.id)
    except Exception as e:
        logger.error(f"Error retrieving subscription status for user {user}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve subscription status"
        )
