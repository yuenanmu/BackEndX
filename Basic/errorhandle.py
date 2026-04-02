from fastapi import FastAPI,HTTPException
app=FastAPI()
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/news/{id}")
async def get_news(id:int):
    id_list=[1,2,3,4]
    if id in id_list:
        return {"news_id":id,"title":f"这是第{id}条新闻","content":f"这是第{id}条新闻的内容"}
    else:
        raise HTTPException(status_code=404,detail="新闻不存在")