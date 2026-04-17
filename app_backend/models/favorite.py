from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

from app_backend.models.news import News
from app_backend.models.users import User

class Base(DeclarativeBase):
    pass

class Favorite(Base):
    """
    收藏表ORM模型
    """
    __tablename__="favorite"
    __table_args__=(
        Index("idx_user_news", "user_id", "news_id", unique=True),  # 用户-新闻唯一索引
    )
    # 创建索引
    # __table_args__ = (
    #     UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
    #     Index(name='fk_favorite_user_idx', expressions='user_id'),
    #     Index(name='fk_favorite_news_idx', expressions='news_id'),
    # )
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    user_id:Mapped[int]=mapped_column(Integer,ForeignKey(User.id),nullable=False,comment="用户ID")
    news_id:Mapped[int]=mapped_column(Integer,ForeignKey(News.id),nullable=False,comment="新闻ID")
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        insert_default=func.now(),
        server_default=func.now(),
        comment="记录创建时间"
        )
    