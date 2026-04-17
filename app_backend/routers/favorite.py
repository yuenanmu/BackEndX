from fastapi import APIRouter, Depends, HTTPException, Query, status

from app_backend.config.db_conf import get_db
from app_backend.crud import favorite
from app_backend.models.users import User
from app_backend.schemas.favorite import FavoriteAddRequest, FavoriteCheckResponse, FavoriteListResponse
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
@router.delete("/remove")
async def remove_favorite(
    news_id:int=Query(...,alias="newsId",description="新闻ID"),
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    result=await favorite.delete_news_favorite(db,user.id,news_id)
    if not result:
        raise HTTPException(404,"收藏记录不存在")
    return success_response(message="收藏成功")

@router.get("/list")
async def get_favorite_lsit(
    page:int=Query(1,ge=1),
    page_size:int=Query(10,ge=1,le=100,alias="pageSize",description="每页记录数"),
    user:User=Depends(get_current_user),
    db:AsyncSession=Depends(get_db)
):
    total,rows=await favorite.get_news_favorite_list(db,user.id,page,page_size)
    has_more=page*page_size<total
    favorite_list=[
        {
            **news.__dict__,#展开News实例的属性到字典中
            "favorite_time":favorite_time,
            "favorite_id":favorite_id
        }
        for news,favorite_time,favorite_id in rows
    ]#列表推导式，把结果变成字典的列表
    response_data=FavoriteListResponse(
        list=favorite_list,
        total=total,
        has_more=has_more
    )
    return success_response(message="成功获取收藏列表", data=response_data)
    
