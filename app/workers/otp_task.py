from workers.queue import Celery_app
import random
import time

@Celery_app.task(name="workers.otp_tasks.send_otp_task")
def send_otp_task(mobile_number, otp_code):
    """
    Mock OTP sending task.
    """
    print(f"[OTP Task] Sending OTP {otp_code} to {mobile_number}")
    # Simulate sending delay
    time.sleep(1)
    return f"OTP {otp_code} sent to {mobile_number}"
