from redis.exceptions import RedisError
import json

from api_v1.redis.redis_client import redis_client


async def publish_message(chat_id: int, message_data: dict):
    try:
        await redis_client.publish(f"chat:{chat_id}", json.dumps(message_data))
    except RedisError as error:
        print(f"[Redis] Publication Error: {error}")


async def listen_for_message(manager):
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("chat:*")
    print(f"[Redis] Listening to all chats: chat:*")

    async for message in pubsub.listen():
        if message["type"] != "pmessage":
            continue
        try:
            channel = message["channel"]
            chat_id = int(channel.split(":")[1])
            data = json.loads(message["data"])

            await manager.send_to_room(chat_id, json.dumps(data))
        except Exception as exception:
            print(f"[Redis] Listener Error:{exception}")
