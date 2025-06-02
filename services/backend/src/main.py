from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from api_v1 import router as router_chat_groups

from core.models.db_helper import db_helper
from core.models.base import Base
from api_v1 import router

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_helper.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
app.include_router(router_chat_groups, prefix="/api")




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
