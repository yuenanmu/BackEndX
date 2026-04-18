from fastapi import APIRouter, Depends

from app_backend.config.db_conf import get_db
from app_backend.models.users import User
from app_backend.schemas.history import HistoryAddRequest
from app_backend.utils.auth import get_current_user
from app_backend.utils.response import success_response
from app_backend.crud import history

from sqlalchemy.ext.asyncio import AsyncSession



router=APIRouter(prefix="/api/history",tags=["history"])

@router.post("/add")
async def add_history(
    data:HistoryAddRequest,
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    response_data=await history.add_news_history(db,user.id,data.news_id)
    return success_response(message="成功添加浏览记录", data=response_data)
