from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from schemas.user import UserResponse
from models.user import User
from core.auth_utils import get_current_user
from core.logger import logger

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

        return user  
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in /user/me: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": "Failed to fetch user profile"}
        )
