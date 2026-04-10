from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.news import Category#导入自定义的模型类Category
async def get_news_categories(db:AsyncSession, skip: int = 0, limit: int = 10):
    query_stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(query_stmt)
    categories=result.scalars().all()
    return categories#这是一个Category类型的列表，包含了查询到的所有Category对象
    