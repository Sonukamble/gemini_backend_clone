from fastapi import APIRouter, Depends, HTTPException, status
from starlette.responses import JSONResponse

from app.schemas.user import UserResponse
from app.models.user import User
from app.core.auth_utils import get_current_user
from app.core.logger import logger

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    """
    Get the authenticated user's profile.

    Returns:
        UserResponse: Basic user details (id, name, mobile number).
    """
    try:
        if not user:
            logger.warning("Authenticated user not found in request context")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")

        user_response={
            "id": user.id,
            "name": user.name,
            "mobile_number": user.mobile_number
        }
        return JSONResponse(status_code=status.HTTP_200_OK, 
                            content={
                                "message": "User profile fetched successfully",
                                "user": user_response
                            })
    except Exception as e:
        logger.error(f"Unexpected error in /user/me: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Failed to fetch user profile Internal Server Error",
                }
        )
