from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from api.auth import auth_router
from api.user import user_router

app = FastAPI(
    title="gemini_backend_clone",
    version="1.0.0",
    description="A clone of the Gemini backend service",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Page not found"
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error"
        }
    }
)

# CORS Middleware configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(auth_router)
app.include_router(user_router)