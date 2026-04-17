from pydantic import BaseModel, Field

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