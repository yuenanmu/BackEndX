from pydantic import BaseModel, Field

class FavoriteCheckResponse(BaseModel):
    """
    收藏表Pydantic模型
    """
    is_favorite:bool=Field(...,alias="isFavorite",description="是否已收藏")