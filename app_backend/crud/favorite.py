from sqlalchemy.ext.asyncio import AsyncSession#异步引擎模块，导入异步会话类
from sqlalchemy import delete, select
from app_backend.models.favorite import Favorite


async def is_news_favorite(db:AsyncSession,user_id:int,news_id:int):
    query_stmt=select(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result=await db.execute(query_stmt)
    favorite=result.scalar_one_or_none()
    return favorite is not None
async def add_news_favorite(db:AsyncSession,user_id:int,news_id:int):
    new_favorite=Favorite(user_id=user_id,news_id=news_id)#其他字段会自动添加默认值
    db.add(new_favorite)#不是异步操作！！不需要await
    await db.commit()#提交事务，必须await（此时不刷新也可以返回ID字段）
    await db.refresh(new_favorite)#刷新实例以获取数据库生成的字段值（如时间戳）

    return new_favorite#因为刷新了，所以这个new_favorite生效了

async def delete_news_favorite(db:AsyncSession,user_id:int,news_id:int):
    #先查（query）再删除(remove)
    delete_stmt=delete(Favorite).where(Favorite.user_id==user_id,Favorite.news_id==news_id)
    result=await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount>0#返回是否删除成功（即是否存在该收藏记录）