#导入declarative_base->定义Base类（继承declarative_base）->定义模型类（继承Base）
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
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

