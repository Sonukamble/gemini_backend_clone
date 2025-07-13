from pydantic import BaseModel, Field
from typing import Optional, Literal


class SignupRequest(BaseModel):
    """
    Request schema for user signup.
    """
    mobile_number: str = Field(..., example="9876543210")
    name: Optional[str] = Field(None, example="John Doe")


class SendOTPRequest(BaseModel):
    """
    Request schema to send OTP.
    """
    mobile_number: str = Field(..., example="9876543210")
    purpose: Literal["login", "reset_password"] = Field(..., example="login")


class VerifyOTPRequest(BaseModel):
    """
    Request schema to verify OTP.
    """
    mobile_number: str = Field(..., example="9876543210")
    otp: str = Field(..., example="1234")
    purpose: Literal["login", "reset_password"] = Field(..., example="login")


class ForgotPasswordRequest(BaseModel):
    """
    Request schema for forgot password flow.
    """
    mobile_number: str = Field(..., example="9876543210")


class ChangePasswordRequest(BaseModel):
    """
    Request schema to change password after verification.
    """
    new_password: str = Field(..., min_length=6, example="MyNewSecurePassword123")


class TokenResponse(BaseModel):
    """
    Response schema for access token generation.
    """
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5...")
    token_type: str = Field(default="bearer", example="bearer")