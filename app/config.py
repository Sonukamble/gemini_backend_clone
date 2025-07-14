import os
from dotenv import load_dotenv
load_dotenv()



class Config:
    # Environment configuration
    # HOST_IP = os.getenv("HOST_IP")
    # HOST_PORT = int(os.getenv("HOST_PORT", 8000))  # Default to 8000 if not specified

    # Database configuration
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")

    # JWT configuration
    SECRET_KEY = os.getenv("SECRET_KEY")    
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Default to 30 minutes if not specified

    REDIS_URL = os.getenv("REDIS_URL") 

    # Stripe configuration
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    STRIPE_PRO_PRICE_ID = os.getenv("STRIPE_PRO_PRICE_ID")
    FRONTEND_URL = os.getenv("FRONTEND_URL")

    # gemini configuration
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    

    
