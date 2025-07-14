# gemini_backend_clone
Gemini-style backend with OTP auth, chatrooms, Gemini AI integration, and Stripe subscriptions – built using FastAPI &amp; Celery.

<!-- project_structure -->

gemini_backend_clone/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app initialization
│   ├── config.py             # Load environment variables, settings
│
│   ├── core/                 # Core utils (JWT, OTP, auth, middleware)
│   │   ├── auth.py
│   │   ├── auth_utils.py
│   │   ├── jwt.py
│   │   ├── otp.py
│   │   ├── caching.py
│   │   └── logger.py
│
│   ├── db/                   # Database-related logic
│   │   ├── base.py           # SQLAlchemy Base
│   │   └── session.py        # DB session creation
│   │ 
│   |── models/           # SQLAlchemy models
│   │       ├── user.py
│   │       ├── chatroom.py
│   │       ├── message.py
│   │       ├── otp.py
│   │       └── subscription.py
│   │
│   ├── schemas/              # Pydantic schemas
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── chatroom.py
│   │   ├── message.py
│   │   └── subscription.py
│
│   ├── api/                  # Route definitions
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── chatroom.py
│   │   ├── message.py
│   │   ├── subscription.py
│   │ 
│   ├── services/             # Business logic layer
│   │   ├── auth_service.py
│   │   ├── chatroom_service.py
│   │   ├── limiting.py
│   │   ├── message_service.py
│   │   └── subscription_service.py
│
│   ├── workers/              # Background task processing
│   │   ├── queue.py          # Redis or Celery setup
│   │   |── otp_task.py  # Handles otp send API calls
│   │   |── message_task.py  # Handles Gemini API calls
│
│   ├── integrations/         # Third-party services
│   │   ├── gemini.py         # Google Gemini API wrapper
│   │   └── stripe.py         # Stripe checkout & webhook logic
│
├── alembic/                  # DB migrations
│   ├── versions/
│   └── env.py
│
├── tests/                    # Unit + integration tests (optional for now)
│
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt
├── README.md                 # Docs with setup, deployment, etc.
├── postman_collection.json   # All API endpoints tested via Postman
└── Docker    