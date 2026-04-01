from fastapi import FastAPI,Query

app=FastAPI()
#查询参数Query Parameters:在URL中以?分隔，参数以键值对形式出现，多个参数用&连接，函数参数与查询参数名称一致
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/news")
async def get_news(news_id:int=Query(...,title="新闻ID",description="这是新闻的ID，必须是整数,范围1~100",gt=0,lt=101)):
    return {"news_id":f"这是第{news_id}条新闻"}
@app.get("/news/news_list")
async def get_news_list(skip:int=Query(0,description="跳过的记录数",lt=101),limit:int=Query(10,description="返回的记录数",gt=0,lt=101)):
    return {"skip":skip,
            "limit":limit,
        }
@app.get("/library/books_type")
async def get_books_type(book_type:str=Query("Python开发",description="这是书籍的类型，必须是字符串",min_length=2,max_length=255)):
    return {"book_type":f"这是{book_type}类型的书籍列表"}
@app.get("/library/books_price")
async def get_books_price(book_price:int=Query(...,description="这是书籍的价格，必须是字符串",ge=2,le=255)):
    return {"book_price":f"这是{book_price}价格的书籍列表"}