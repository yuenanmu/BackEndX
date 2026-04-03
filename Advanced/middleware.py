from fastapi import FastAPI


#中间件用于添加一些功能到请求处理过程中，比如日志记录、性能监控、错误处理等。
# 中间件函数接受两个参数：request和call_next。request是当前请求对象，call_next是一个函数，
# 用于调用下一个中间件或最终的请求处理函数。

app=FastAPI()
@app.middleware("http")
async def add_process_time_header1(request,call_next):
    print("middleware1 start")
    response=await call_next(request)
    print("middleware1 end")
    return response

@app.middleware("http")
async def add_process_time_header2(request,call_next):
    print("middleware2 start")
    response=await call_next(request)
    print("middleware2 end")
    return response

@app.get("/")
async def root():
    return {"msg":"Hello World"}