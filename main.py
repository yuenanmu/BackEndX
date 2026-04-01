from fastapi import FastAPI,Path

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/learn")#路由：地址与函数映射关系
async def learn_fastapi():
    return {"msg":"我正在学习FastAPI！"}

#路径参数Path Parameters：在URL路径中定义参数，使用{}括起来，函数参数与路径参数名称一致
@app.get("/book_num/{book_id}")
async def get_book(book_id:int):
    return {"book_id":f"这是我的第{book_id}本书"}
@app.get("/book_details/{book_id}")
async def get_book_details(book_id:int=Path(...,title="书籍ID",description="这是书籍的ID，必须是整数,范围1~100",gt=0,lt=101)):
    return {"book_id":f"这是第{book_id}本书的详细信息"}
@app.get("/author/{author_name}")
async def get_author(author_name:str=Path(...,description="这是作者的名字，必须是字符串",min_length=2,max_length=50)):
    return {"author_name":f"这是作者{author_name}的详细信息"}
@app.get("/news/{news_id}")
async def get_news(news_id:int=Path(...,title="新闻ID",description="整型，范围1~100",gt=0,lt=101)):
    return {
        "news_id":f"这是第{news_id}条新闻"
    }
@app.get("/news_details/{news_name}")
async def get_news_details(news_name:str=Path(...,title="新闻名称",description="这是新闻名称",min_length=2,max_length=100)):
    return {
        "news_id":f"这是about{news_name}新闻的详细信息"
    }
#查询参数Query Parameters:在URL中以?分隔，参数以键值对形式出现，多个参数用&连接，函数参数与查询参数名称一致
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}