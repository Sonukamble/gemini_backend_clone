from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.user import User
from models.otp import OTP
from core.otp import generate_otp
from core.jwt import create_access_token
from core.auth import hash_password
from core.logger import logger

from datetime import datetime, timedelta
import uuid
from typing import Optional

def signup_user(db: Session, mobile_number: str, name: Optional[str] = None) -> Optional[User]:
    """
    Registers a new user in the system.
    """
    try:
        user = User(id=str(uuid.uuid4()), mobile_number=mobile_number, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User signed up: {mobile_number}")
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error signing up user {mobile_number}: {e}")
        return None
    

def send_otp(db: Session, user_id: str, purpose: str) -> Optional[str]:
    """
    Generates and stores a new OTP for a user.
    """
    try:
        otp_code = generate_otp()
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        otp_entry = OTP(
            id=str(uuid.uuid4()),
            user_id=user_id,
            otp_code=otp_code,
            purpose=purpose,
            expires_at=expires_at
        )
        db.add(otp_entry)
        db.commit()
        logger.info(f"OTP sent for user {user_id}, purpose={purpose}")
        return otp_code
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Failed to send OTP for user {user_id}: {e}")
        return None
    

def verify_otp(db: Session, mobile_number: str, otp_code: str, purpose: str) -> Optional[str]:
    """
    Verifies a user's OTP and returns an access token.
    """
    try:
        user = db.query(User).filter(User.mobile_number == mobile_number).first()
        if not user:
            logger.warning(f"User not found for mobile: {mobile_number}")
            return None

        otp_entry = db.query(OTP).filter(
            OTP.user_id == user.id,
            OTP.otp_code == otp_code,
            OTP.purpose == purpose,
            OTP.expires_at >= datetime.utcnow(),
            OTP.is_verified == False
        ).first()

        if not otp_entry:
            logger.warning(f"Invalid or expired OTP for user {mobile_number}")
            return None

        otp_entry.is_verified = True
        db.commit()

        access_token = create_access_token(data={"user_id": user.id})
        logger.info(f"OTP verified and token issued for {mobile_number}")
        return access_token
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"OTP verification failed for {mobile_number}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during OTP verification: {e}")
        return None
    


def change_password(db: Session, user: User, new_password: str) -> Optional[User]:
    """
    Changes the password of a given user.
    """
    try:
        hashed = hash_password(new_password)
        if not hashed:
            logger.error(f"Password hashing failed for user {user.id}")
            return None

        user.password_hash = hashed
        db.commit()
        db.refresh(user)
        logger.info(f"Password changed for user {user.id}")
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error changing password for user {user.id}: {e}")
        return None