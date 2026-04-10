from fastapi import FastAPI
from app_backend.routers import news
import traceback
import sys

# 强制打印所有错误
def catch_exceptions(exc_type, exc_value, exc_traceback):
    traceback.print_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = catch_exceptions
app = FastAPI(debug=True)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
#挂载模块化的路由（各个模块的接口）
app.include_router(news.router)