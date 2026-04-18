from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.models.history import History
from app_backend.models.news import News
async def add_news_history(db:AsyncSession,user_id:int,news_id:int):
    new_history=History(user_id=user_id,news_id=news_id)
    db.add(new_history)
    await db.commit()
    await db.refresh(new_history)

    return new_history

async def get_news_history_list(db:AsyncSession,user_id:int,page:int,page_size:int):
    #统计总量
    count_stmt=select(func.count()).where(History.user_id==user_id)
    count_result=await db.execute(count_stmt)
    total=count_result.scalar_one()#把对象抓包为int型
    #查询数据
    query_stmt=(
        select(News, History.view_time.label("view_time"), History.id.label("history_id"))
        .join(History, History.news_id==News.id)
        .where(History.user_id==user_id)
        .order_by(History.view_time.desc())
        .offset((page-1)*page_size)
        .limit(page_size)
    )
    query_result=await db.execute(query_stmt)
    rows=query_result.all()
    return total,rows
async def delete_news_history(db:AsyncSession,user_id:int,history_id:int):
    delete_stmt=(
        delete(History)
        .where(History.id==history_id,History.user_id==user_id)
    )
    delete_result=await db.execute(delete_stmt)
    await db.commit()
    return delete_result.rowcount>0