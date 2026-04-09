from fastapi import APIRouter

router=APIRouter(prefix="/api/news",tags=["新闻相关接口"])

@router.get("/categories")
async def get_news_categories():
    return {"message":"这是新闻分类接口"}