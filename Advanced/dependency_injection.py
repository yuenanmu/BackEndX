from fastapi import FastAPI, Query,Depends

app=FastAPI()

#依赖注入是一种设计模式，用于实现组件之间的解耦。在FastAPI中，依赖注入可以通过Depends函数来实现。
#依赖注入函数可以接受参数，这些参数可以是请求参数、路径参数
#或者其他依赖注入函数的返回值。FastAPI会自动解析这些参数，并将它们传递给依赖注入函数。
def common_func(
        skip:int=Query(0,ge=0,description="skip offset"),
        limit:int=Query(10,lt=60)
):
    return {"skip":skip,"limit":limit}

#url="GET /items/?skip=2&limit=10 HTTP/1.1"
@app.get("/items/")
async def read_items(commons:dict=Depends(common_func)):
    print("read_items")
    print(commons)
    return commons
@app.get("/users/")
async def read_users(commons=Depends(common_func)):
    print("read_users")
    print(commons)
    return commons

