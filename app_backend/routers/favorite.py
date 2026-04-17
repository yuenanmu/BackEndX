from fastapi import APIRouter, Depends, Query

from app_backend.config.db_conf import get_db
from app_backend.crud import favorite
from app_backend.models.users import User
from app_backend.schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse
from app_backend.utils.auth import get_current_user

from sqlalchemy.ext.asyncio import AsyncSession

from app_backend.utils.response import success_response

router=APIRouter(prefix="/api/favorite",tags=["favorite"])
@router.get("/check")
async def check_favorite(
    news_id:int=Query(...,alias="newsId",description="新闻ID"),
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    is_fav=await favorite.is_news_favorite(db,user.id,news_id)
    return success_response(data=FavoriteCheckResponse(isFavorite=is_fav))
@router.post("/add")
async def add_favorite(
    data:FavoriteAddRequest,
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    result=await favorite.add_news_favorite(db,user.id,data.news_id)
    return success_response(message="收藏成功",data=result)
    
