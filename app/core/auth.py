from passlib.context import CryptContext
from typing import Optional

from app.core.logger import logger
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        raise

# def get_password_hash(password: str) -> str:
#     """
#     Returns the hashed version of the password.

#     Args:
#         password (str): The plain password to hash.

#     Returns:
#         str: The hashed password.
#     """
#     return hash_password(password)  


# def check_password_strength(password: str) -> bool:
#     """
#     Checks the strength of a password.

#     Args:
#         password (str): The password to check.

#     Returns:
#         bool: True if the password is strong, False otherwise.
#     """
#     if len(password) < 8:
#         return False
#     if not any(char.isdigit() for char in password):
#         return False
#     if not any(char.isalpha() for char in password):
#         return False
#     return True 


