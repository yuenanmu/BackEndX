from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/learn")#路由：地址与函数映射关系
async def learn_fastapi():
    return {"msg":"我正在学习FastAPI！"}

@app.get("/book/{book_id}")
async def return_book(book_id:int):
    return {"book_id":f"这是我的第{book_id}本书"}