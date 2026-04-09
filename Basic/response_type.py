from fastapi import FastAPI
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse
from pydantic import BaseModel

app=FastAPI()
#修饰器中指定响应类型，一般是HTML和文本
html_content="</h1>这是一个HTML响应</h1>"
@app.get("/html",response_class=HTMLResponse)#,response_class=HTMLResponse
async def get_html():
    return html_content

#return返回指定响应类型,包含图片，视频，excel,PPT等文件
@app.get("/file")
async def get_file():
    file_path="./files/1.webp"
    return FileResponse(file_path)

#自定义响应格式
class News(BaseModel):
    news_id:int 
    title:str
    content:str
@app.get("/news/{news_id}",response_model=News)#约定了响应格式,校验响应数据,过滤多余字段
async def get_news(news_id:int):
    return {
        "news_id":news_id,
        "title":f"这是第{news_id}条新闻的标题",
        "content":f"这是第{news_id}条新闻的内容"
    }
    # FastAPI 会自动把它变成 News 模型，并且只返回 news_id + title
    # 多返回字段会被删掉！！!   


