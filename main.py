from fastapi import FastAPI
from app_backend.routers import news

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
#挂载模块化的路由（各个模块的接口）
app.include_router(news.router)