from datetime import datetime, timedelta

from core.caching import redis

# Initialize Redis connection (adjust host/port/db as needed)
from fastapi import HTTPException, status

PROMPT_LIMIT_BASIC = 5

async def check_prompt_limit(user_id: str, tier: str):
    if tier.lower() == "pro":
        return  # Pro users have no limit

    # Create key like daily_prompts:123:20250714
    today = datetime.utcnow().strftime("%Y%m%d")
    key = f"daily_prompts:{user_id}:{today}"

    # Increment counter in Redis
    count = await redis.incr(key)

    if count == 1:
        # Set TTL to expire at midnight UTC
        now = datetime.utcnow()
        tomorrow = datetime(now.year, now.month, now.day) + timedelta(days=1)
        ttl = int((tomorrow - now).total_seconds())
        await redis.expire(key, ttl)

    if count > PROMPT_LIMIT_BASIC:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Daily prompt limit reached for Basic tier. Upgrade to Pro for unlimited access."
        )
