import redis.asyncio as redis
from redis.exceptions import RedisError
from config import settings

redis_client = redis.Redis(host=settings.host, port=settings.port, decode_responses=True)


MAX_MESSAGES = 50

async def save_message(subject: int, message: str):
    key = f"chat:{subject}"
    try:
        await redis_client.rpush(key, message)
        await redis_client.ltrim(key, -MAX_MESSAGES, -1)
    except RedisError as error:
        print(f"[Redis] Ошибка при сохранении сообщения в {key}: {error}")
    except Exception as error:
        print(f"[System] Неизвестная ошибка в save_message: {error}")


async def get_history(subject: int, limit: int = 20):
    key = f"chat:{subject}"
    try:
        return await redis_client.lrange(key, -limit, -1)
    except RedisError as error:
        print(f"[Redis] Ошибка при получении истории из {key}: {error}")
        return []
    except Exception as error:
        print(f"[System] Неизвестная ошибка в get_history: {error}")
        return []