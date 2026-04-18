from pydantic import BaseModel, Field

from app_backend.schemas.base import NewsItemBase

class HistoryAddRequest(BaseModel):
    news_id:int=Field(...,alias="newsId")

class HistoryNewsItem(NewsItemBase):
    view_time:str=Field(...,alias="viewTime")
    history_id:int=Field(...,alias="historyId")


class HistoryListResponse(BaseModel):
    list:list[HistoryNewsItem]
    total:int
    has_more:bool=Field(...,alias="hasMore")
