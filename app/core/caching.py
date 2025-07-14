from fastapi import HTTPException
from redis import asyncio as aioredis
from typing import Optional, List
import json
import os

from app.core.logger import logger
from app.config import Config


# Create Redis connection
try:
    redis = aioredis.from_url(Config.REDIS_URL, decode_responses=True)
except Exception as e:
    logger.error("Failed to connect to Redis", exc_info=True)
    raise HTTPException(
        status_code=500,
        detail="Redis connection error"
    )


async def get_cached_chatrooms(user_id: int) -> Optional[List[dict]]:
    """Retrieve cached chatrooms for a user from Redis"""
    try:
        if not redis:
            raise ConnectionError("Redis connection is not established")
        
        key=f"chatrooms:{user_id}"
        data= await redis.get(key)
        if data:
            logger.info(f"Retrieved cached chatrooms for user {user_id}")
            return json.loads(data)
        logger.info(f"Cache miss for user {user_id}")
        return None
    except Exception as e:
            logger.error(f"Error retrieving cached chatrooms for user {user_id}: {e}")
            return None
    
    

async def set_cached_chatrooms(user_id: int, chatrooms: list, ttl: int = 600)-> None:
    """Set cached chatrooms for a user in Redis"""
    try: 
        if not redis:
            raise ConnectionError("Redis connection is not established")
        
        key = f"chatrooms:{user_id}"
        await redis.set(key, json.dumps(chatrooms, default=str), ex=ttl)
        logger.info(f"Cached chatrooms for user {user_id} with TTL {ttl} seconds")
    except Exception as e:
        logger.error(f"Error setting cached chatrooms for user {user_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to set cached chatrooms"
        )   
         