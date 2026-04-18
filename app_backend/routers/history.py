from fastapi import APIRouter, Depends, Query

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
@router.get("/list")
async def get_history_list(
    page:int=Query(1,ge=1),
    page_size:int=Query(10,ge=1,le=100,
                    alias="pageSize"),
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    total,rows=await history.get_news_history_list(db,user.id,page,page_size)
    history_list=[
        {
            **news.__dict__,
            "view_time":view_time,
            "history_id":history_id,
            
        }
        for news,view_time,history_id  in rows
    ]
    response_data={
        "total":total,
        "has_more":total>page*page_size,
        "history_list":history_list
    }
    return success_response(message="成功获取浏览记录列表", data=response_data)