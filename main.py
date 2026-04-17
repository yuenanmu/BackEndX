from fastapi import FastAPI
from app_backend.routers import favorite, news, users
from fastapi.middleware.cors import CORSMiddleware

from app_backend.utils.exception_handlers import register_exception_handlers
# import traceback
# import sys

# # 强制打印所有错误
# def catch_exceptions(exc_type, exc_value, exc_traceback):
#     traceback.print_exception(exc_type, exc_value, exc_traceback)

# sys.excepthook = catch_exceptions
# app = FastAPI(debug=True)
app = FastAPI()

# 注册全局异常处理器
register_exception_handlers(app)

#添加CORS中间件，解决跨域问题：协议、端口、域名都要一致才允许
origins=[
    "http://localhost:3000",
    "http://localhost:8000",
    ""
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源,实际应用时，需要自定义允许的源列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP请求方法：request,post,put,delete等
    allow_headers=["*"],  # 允许所有HTTP头
)

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
#挂载模块化的路由（各个模块的接口）
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
#运行指令
# uvicorn main:app --reload
# cd app_frontend->npm run dev