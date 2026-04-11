from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app_backend.models.news import Category, News#导入自定义的模型类Category和News
async def get_news_categories(db:AsyncSession, skip: int = 0, limit: int = 10):
    query_stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(query_stmt)
    categories=result.scalars().all()
    return categories#这是一个Category类型的列表，包含了查询到的所有Category对象
async def get_news_list(db:AsyncSession,category_id: int, skip: int = 0, limit: int = 10):
    #查询指定分类下的新闻
    query_stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(query_stmt)
    news_list=result.scalars().all()
    return news_list
#查询这个类别下的新闻总数
async def get_news_num(db:AsyncSession,category_id: int):
    query_stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(query_stmt)
    total=result.scalar_one()
    return total
async def get_news_details(db:AsyncSession,news_id:int):
    query_stmt=select(News).where(News.id==news_id)
    result=await db.execute(query_stmt)
    new_details=result.scalar_one_or_none()
    return new_details
async def increase_news_views(db:AsyncSession,news_id:int):
    update_stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(update_stmt)
    await db.commit()
    return result.rowcount>0
async def get_related_news(db:AsyncSession,news_id:int,category_id:int, limit: int = 5):
    #查询同一分类下的相关新闻，排除当前新闻，并按照发布时间降序排序!.order_by().limit()神来之笔！
    query_stmt=select(News).where(News.category_id==category_id,News.id!=news_id).order_by(News.publish_time.desc()).limit(limit)
    result=await db.execute(query_stmt)
    related_news=result.scalars().all()
    return related_news