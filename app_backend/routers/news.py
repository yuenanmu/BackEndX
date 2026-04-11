from fastapi import APIRouter, Depends, Query
from app_backend.crud import news
from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.config.db_conf import get_db
#创建一个APIRouter实例，设置前缀prefix和标签tags
router=APIRouter(prefix="/api/news",tags=["新闻相关接口"])
#接口实现流程
#1.模块化路由
#2.设计模型类
#3.crud中实现增删改查方法
#4.在路由处理函数中调用crud函数实现接口功能



@router.get("/categories")
async def get_news_categories(db: AsyncSession=Depends(get_db), skip: int = 0, limit: int = 10):
    categories=await news.get_news_categories(db, skip, limit)
    return {"code":200, 
            "skip": skip, 
            "limit": limit,
            "message":"这是新闻分类接口",
            "data": categories
        }

@router.get("/list")
async def get_news_list(
    db: AsyncSession=Depends(get_db),
    category_id:int=Query(...,alias="categoryId", description="新闻分类ID"),
    page: int = Query(1,ge=1, description="页码,从1开始"),
    page_size: int = Query(10,alias="pageSize")
):
    offset=(page-1)*page_size
    news_list=await news.get_news_list(db, category_id, offset, page_size)
    total=await news.get_news_num(db, category_id)
    has_more=offset+len(news_list)<total
    return {"code":200, 
            "message":"这是新闻列表接口",
            "data": {
                "list": news_list,#"新闻列表",#
                "total": total,
                "hasMore": has_more
                }
        }
