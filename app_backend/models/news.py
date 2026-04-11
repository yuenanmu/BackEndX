#导入declarative_base->定义Base类（继承declarative_base）->定义模型类（继承Base）
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column


class Base(DeclarativeBase):
    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        insert_default=func.now(),
        server_default=func.now(),
        comment="记录创建时间"
        )
    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        insert_default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        comment="记录更新时间"
        )
    
class Category(Base):
    __tablename__="news_category"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String(50),unique=True,nullable=False,comment="分类名称")
    sort_order:Mapped[int]=mapped_column(Integer,default=0,nullable=True,comment="分类描述")
    #定义__repr__方法，方便调试和日志记录。否则返回地址
    def __repr__(self):
        return f"<Category(id={self.id},name={self.name},sort_order={self.sort_order})>"

class News(Base):
    __tablename__="news"
    #创建索引，提升性能
    __table_args__=(
         Index("fk_news_category_id", "category_id"),  # 高频查询对象
        Index("idx_publish_time", "publish_time"),    # 按照时间排序
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False)
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
