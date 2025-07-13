import datetime

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError

from core.logger import logger
from config import Config


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> Optional[str]:
    """
    Creates a JWT access token.

    Args:
        data (Dict[str, Any]): The payload to encode into the JWT.
        expires_delta (Optional[timedelta]): Expiration time delta.

    Returns:
        Optional[str]: Encoded JWT token, or None if error occurs.
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create JWT: {e}")
        return None
    
def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifies and decodes a JWT token.

    Args:
        token (str): JWT token string.

    Returns:
        Optional[Dict[str, Any]]: Decoded payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=Config.ALGORITHM)
        return payload
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {e}")
        return None