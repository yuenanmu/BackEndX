from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.models.history import History
async def add_news_history(db:AsyncSession,user_id:int,news_id:int):
    new_history=History(user_id=user_id,news_id=news_id)
    db.add(new_history)
    await db.commit()
    await db.refresh(new_history)

    return new_history