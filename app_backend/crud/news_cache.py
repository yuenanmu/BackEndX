from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app_backend.cache.news_cache import get_cached_categories, get_cached_news_list, set_cache_categories, set_cache_news_list
from app_backend.models.news import Category, News
from app_backend.schemas.base import NewsItemBase#导入自定义的模型类Category和News
#普通的异步函数不需要进行依赖注入！直接传入db参数即可！不需要Depends(get_db)！
# 因为这是一个纯粹的数据库操作函数，不涉及到HTTP请求的处理，所以不需要依赖注入来获取数据库会话对象！
# 只要在调用这个函数时传入一个有效的AsyncSession对象就可以了！
# 这样设计可以让这个函数更加灵活，可以在不同的上下文中使用，而不仅仅局限于FastAPI的请求处理过程中！
async def get_news_categories(db:AsyncSession, skip: int = 0, limit: int = 10):
    #从缓存中查询所有分类
    cached_categories=await get_cached_categories()
    if cached_categories:
        #print("✌️成功从缓存中查询分类")
        return cached_categories
    #数据库中查询所有分类
    query_stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(query_stmt)
    categories=result.scalars().all()
    #写入缓存
    if categories:
        categories=jsonable_encoder(categories)
        await set_cache_categories(categories)
        #print("✌️成功从数据库查询分类并写入缓存")
    return categories#这是一个Category类型的列表，包含了查询到的所有Category对象
async def get_news_list(db:AsyncSession,category_id: int, skip: int = 0, limit: int = 10):
    #先从缓存中查询这个分类下的新闻列表
    page=skip//limit+1
    cached_news_list=await get_cached_news_list(category_id, page, limit)
    if cached_news_list:
        #print("✌️成功从缓存中查询新闻列表")
        #转换为News对象列表
        return [News(**item) for item in cached_news_list]
    #查询指定分类下的新闻
    query_stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(query_stmt)
    news_list=result.scalars().all()
    #写入缓存
    if news_list:
        #ORM->Pydantic->JSON()
        news_data=[NewsItemBase.model_validate(item).model_dump(mode="json",by_alias=False) for item in news_list]
        await set_cache_news_list(category_id, page, limit, news_data)
        #print("✌️成功从数据库查询新闻列表并写入缓存")
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
    related_news_msg=[{
        "id": new_details.id,
        "title": new_details.title,
        "content": new_details.content,
        "image": new_details.image or "null",
        "author": new_details.author or "null",
        "publishTime": new_details.publish_time or "2023-01-01T00:00:00",
        "categoryId": new_details.category_id,
        "views": new_details.views,
    }
     for new_details in related_news]
    return related_news_msg