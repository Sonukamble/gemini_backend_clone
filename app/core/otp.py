import secrets
from typing import Union

def generate_otp(length: int = 4) -> str:
    """
    Generates a secure numeric OTP (One-Time Password).

    Args:
        length (int): Length of the OTP to generate. Must be a positive integer.

    Returns:
        str: A string containing the numeric OTP.
    
    Raises:
        ValueError: If the length is not a positive integer.
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("OTP length must be a positive integer.")
    
    return ''.join(secrets.choice("0123456789") for _ in range(length))
