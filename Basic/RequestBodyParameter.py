from fastapi import FastAPI
from pydantic import BaseModel,Field
#请求体参数Request Body Parameters：在请求体中定义参数，使用Pydantic模型来定义数据结构
app=FastAPI()
class Book(BaseModel):
    title:str=Field(...,min_length=2,max_length=20,description="书名，字符串类型，长度2~20")
    author:str=Field(...,min_length=2,max_length=10,description="作者，字符串类型，长度2~10")
    publisher:str=Field("小杜出版社",min_length=0,description="出版社，字符串类型，默认为小杜出版社")
    price:float=Field(...,gt=0,description="价格，浮点数类型，必须大于0")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
@app.post("/library")
async def post_book_msg(book:Book):
    return book