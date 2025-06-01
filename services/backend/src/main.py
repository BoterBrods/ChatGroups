from fastapi import FastAPI
import uvicorn
from api_v1 import router as router_chat_groups

app = FastAPI()

app.include_router(router_chat_groups, prefix='/api')

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)