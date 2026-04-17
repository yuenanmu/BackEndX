from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from app_backend.schemas.base import NewsItemBase
class FavoriteCheckResponse(BaseModel):
    """
    收藏表Pydantic模型
    """
    is_favorite:bool=Field(...,alias="isFavorite",description="是否已收藏")

class FavoriteAddRequest(BaseModel):
    """
    添加收藏请求模型
    """
    news_id:int=Field(...,alias="newsId",description="新闻ID")

#规划两个类（用继承的形式）：一个新闻模型类+一个收藏模型类
class FavoriteNewsItemResponse(NewsItemBase):
    """
    收藏列表新闻项模型
    """
    favorite_id:int=Field(...,alias="favoriteId")
    favorite_time:datetime=Field(...,alias="favoriteTime")
    
    model_config=ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

#收藏列表响应接口
class FavoriteListResponse(BaseModel):
    """
    收藏列表响应模型
    """
    list:list[FavoriteNewsItemResponse]
    total:int
    has_more:bool=Field(...,alias="hasMore")

    model_config=ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )