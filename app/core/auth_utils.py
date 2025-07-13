from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from core.jwt import verify_token
from db.session import get_db
from models.user import User
from core.logger import logger  

def get_current_user(
    authorization: str = Header(..., description="Bearer access token"),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to extract and return the currently authenticated user
    from the Authorization header.

    Raises:
        HTTPException: If token is invalid or user is not found.

    Returns:
        User: The authenticated user from the database.
    """
    try:
        if not authorization.startswith("Bearer "):
            logger.warning("Authorization header missing 'Bearer' prefix")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )

        token = authorization.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            logger.warning("JWT token verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )

        user = db.query(User).filter(User.id == payload.get("user_id")).first()
        if not user:
            logger.warning(f"User not found with ID {payload.get('user_id')}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except HTTPException:
        raise  # Propagate expected errors
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )