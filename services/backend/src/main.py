import asyncio

from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from api_v1 import router as router_chat_groups
from api_v1.redis.pubsub import listen_for_message
from api_v1.websocket.ConnectionManager import manager

from core.models.db_helper import db_helper
from core.models.base import Base
from api_v1 import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    asyncio.create_task(listen_for_message(manager))
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router_chat_groups, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)


