from sqlalchemy.ext.asyncio import AsyncSession#异步引擎模块，导入异步会话类
from sqlalchemy import select
from app_backend.models.favorite import Favorite


async def is_favorite(db:AsyncSession,user_id:int,news_id:int):
    query_stmt=select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result=await db.execute(query_stmt)
    favorite=result.scalar_one_or_none()
    return favorite is not None