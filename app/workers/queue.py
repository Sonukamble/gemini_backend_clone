from celery import Celery

from app.config import Config

Redis_URL = Config.REDIS_URL

Celery_app = Celery(
    "gemini_backend_clone", 
    broker=Redis_URL,
    backend=Redis_URL,  
    # include=["gemini_backend_clone.app.workers.queue"]
)

Celery_app.conf.update(
    
    task_routes={
        "workers.otp_tasks.send_otp_task": {
            "queue": "otp_queue"
        },
        "workers.message_task.process_message_response": {
            "queue": "message_queue"
        },
        
    },
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)

