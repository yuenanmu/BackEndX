from sqlalchemy.ext.asyncio import AsyncSession#异步引擎模块，导入异步会话类
from sqlalchemy import delete, func, select
from app_backend.models.favorite import Favorite
from app_backend.models.news import News


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
async def get_news_favorite_list(
        db:AsyncSession,
        user_id:int,
        page:int=1,
        page_size:int=10
):
    #统计总量
    count_stmt=select(func.count()).where(Favorite.user_id==user_id)
    total_result=await db.execute(count_stmt)
    total=total_result.scalar_one()#抓包，得到int型总数

    #分页查询：联表查询+收藏时间排序+分页
    #select(查询主题模型类，附表的字段（需要别名）).join(联表查询的模型类，联合查询条件).where().order_by().offset().limit()
    offset=(page-1)*page_size
    query_stmt=(select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
                    .join(Favorite,Favorite.news_id==News.id)
                    .where(Favorite.user_id==user_id)#缩小范围到当前用户收藏
                    .order_by(Favorite.created_at.desc())
                    .offset(offset).limit(page_size)
                )
    result=await db.execute(query_stmt)
    #[
    #   (News实例，收藏时间，收藏ID),
    #   (News实例，收藏时间，收藏ID),
    #]
    rows=result.all()#得到一个列表，每个元素是一个元组（News实例，收藏时间，收藏ID）
    return total,rows
async def clear_news_favorite(db:AsyncSession,user_id:int):
    delete_stmt=delete(Favorite).where(Favorite.user_id==user_id)
    result=await db.execute(delete_stmt)
    await db.commit()
    return result.rowcount or 0#返回是否清空成功（即是否存在收藏记录）
