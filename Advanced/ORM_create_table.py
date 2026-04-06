from fastapi import Depends, FastAPI
from datetime import datetime
from fastapi.concurrency import asynccontextmanager
from sqlalchemy import DateTime, Float, String,func
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped,mapped_column #Mapped约定属性类型，mapped_column约定属性字段

#创建异步引擎
ASYNC_DATABASE_URL="mysql+aiomysql://root:173059@localhost:3306/FastAPI_first?charset=utf8"
async_engine=create_async_engine(ASYNC_DATABASE_URL,
    echo=True,#optput SQL statemens
    pool_size=5,#连接池活跃用户的大小，默认为5
    max_overflow=10#允许的额外的连接数
)


#定义模型类，用于数据表结构定义
class Base(DeclarativeBase):
    create_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),server_default=func.now(),comment="创建时间")
    update_time:Mapped[datetime]=mapped_column(DateTime,insert_default=func.now(),server_default=func.now(),onupdate=func.now(),comment="更新时间")
    

class Book(Base):
    __tablename__='boooks'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    title:Mapped[str]=mapped_column(String(255),nullable=False,comment="书籍标题")
    author:Mapped[str]=mapped_column(String(255),nullable=False,comment="书籍作者")
    publisher:Mapped[str]=mapped_column(String(255),nullable=False,comment="书籍出版社")
    price:Mapped[float]=mapped_column(Float,nullable=False,comment="书籍价格")

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str]=mapped_column(String(255),nullable=False,comment="用户名")
    password:Mapped[str]=mapped_column(String(255),nullable=False,comment="用户密码")

#创建表
#获取异步引擎，建表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)#用Base的元数据创建表

# @app.on_event("startup")
# async def startup_event():
#     await create_tables()#启动时创建表


# # 👉 新版 lifespan 替代旧版 on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：创建数据库表
    await create_tables()
    print("✅ 服务启动，数据库表已创建")
    
    yield  # 服务运行中
    
    # 关闭时：释放数据库连接
    await async_engine.dispose()
    print("✅ 服务关闭，数据库连接已释放")

# 传入 lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"msg":"Hello World"}
#创建一个查询窗口，查询books表中的数据->创建依赖项获取数据库会话+Depends注入路由处理函数
AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,#绑定异步引擎
    expire_on_commit=False,#提交后会话不失效
    class_=AsyncSession,#指定会话类型
)
#创建依赖项，获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()#提交事务
        except Exception as e:
            await session.rollback()#回滚事务
            raise e
        finally:
            await session.close()#关闭会话

#图书查询接口
@app.get("/library/books")
async def get_books(db:AsyncSession=Depends(get_db)):
    result=await db.execute(sqlalchemy.select(Book))#获取一个ORM查询对象
    books=result.scalars().all()#对象中提取所有的Book实例
    book=result.scalars().first()#提取第一个Book实例

    book_id=await db.get(Book,2)#根据主键查询Book实例
    return book_id