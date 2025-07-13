from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.auth import (
    SignupRequest,
    SendOTPRequest,
    VerifyOTPRequest,
    ChangePasswordRequest,
    TokenResponse,
)
from schemas.user import UserResponse
from services import auth_service
from models.user import User
from core.logger import logger
from core.auth_utils import get_current_user


auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    """
    Register a new user with mobile number and optional name.
    """
    try:
        user = auth_service.signup_user(db, data.mobile_number, data.name)
        if not user:
            raise HTTPException(status_code=500, detail="User signup failed")
        return user
    except Exception as e:
        logger.error(f"Signup error for {data.mobile_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.post("/send-otp", status_code=status.HTTP_200_OK)
def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    """
    Send an OTP for login or password reset.
    """
    try:
        user = db.query(User).filter(User.mobile_number == data.mobile_number).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp_code = auth_service.send_otp(db, user.id, data.purpose)
        if not otp_code:
            raise HTTPException(status_code=500, detail="Failed to generate OTP")

        logger.info(f"OTP sent to {data.mobile_number} for {data.purpose}")
        return {
            "message": "OTP sent successfully",
            "otp": otp_code
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending OTP for {data.mobile_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@auth_router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and return JWT access token.
    """
    try:
        access_token = auth_service.verify_otp(db, data.mobile_number, data.otp, data.purpose)
        if not access_token:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")

        logger.info(f"OTP verified for {data.mobile_number}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification failed for {data.mobile_number}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@auth_router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Change the password for an authenticated user.
    """
    try:
        updated_user = auth_service.change_password(db, user, data.new_password)
        if not updated_user:
            raise HTTPException(status_code=500, detail="Password update failed")

        logger.info(f"Password changed for user {user.id}")
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password for user {user.id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")