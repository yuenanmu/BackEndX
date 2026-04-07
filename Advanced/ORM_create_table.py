from fastapi import Depends, FastAPI, HTTPException, Path
from datetime import datetime
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel
from sqlalchemy import DateTime, Float, String,func, select
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

    book_id=await db.get(Book,3)#根据主键查询Book实例/数据库数据。没有不会报错，返回noll
    return book_id

#图书查询接口，添加路径参数(用【比较判断】筛选一本书籍)
@app.get("/library/books/id/{book_id}")
async def get_book_by_id(book_id:int=Path(...,gt=0,description="书籍ID"),db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(Book).where(Book.id==book_id))#根据路径参数查询Book实例
    book=result.scalar_one_or_none()#提取单个Book实例，如果没有或有多个则返回None
    return book
#图书查询接口，通过【比较判断】价格筛选一本/多本书籍
@app.get("/library/books/price/{price}")
async def get_books_by_price(price:float=Path(...,gt=0,description="筛选大于价格的所有书籍 "),db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(Book).where(Book.price>=price))#根据价格查询Book实例
    books=result.scalars().all()#提取所有匹配价格的Book实例
    return books
#图书查询接口，通过【模糊匹配】筛选一本/多本书籍
@app.get("/library/books/title/{title}")
async def get_books_by_title(title:str=Path(...,description="筛选包含标题的所有书籍"),db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(Book).where(Book.title.like(f"%{title}%")))#根据标题模糊查询Book实例
    books=result.scalars().all()#提取所有匹配标题的Book实例
    return books
#图书查询接口，通过【in_()包含】筛选一本/多本书籍
@app.get("/library/books/id_list")
async def get_book_by_id_list(db:AsyncSession=Depends(get_db)):
    id_list=[1,2,5,7]#要查询的ID列表
    result=await db.execute(select(Book).where(Book.id.in_(id_list)))#根据路径参数查询Book实例
    books=result.scalars().all()#提取单个Book实例，如果没有或有多个则返回None
    return books
#图书统计接口，通过【聚合查询】统计书籍数量、平均价格和总价格
@app.get("/library/books/calculate")
async def calculate_book(db:AsyncSession=Depends(get_db)):
    result=await db.execute(select(func.count(Book.id),func.avg(Book.price),func.sum(Book.price),func.max(Book.price)))#统计书籍数量和平均价格
    count,avg_price,sum_price,max_price=result.fetchone()#提取统计结果
    return {"count":count,"avg_price":round(avg_price, 2),"sum_price":round(sum_price, 2),"max_price":round(max_price, 2)}
#图书分页查询接口，通过【offset和limit】实现分页查询
@app.get("/library/books/slice/page_slice")
async def get_books_page_slice(
    page: int = 1, 
    page_size: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    skip=(page-1)*page_size#跳过的记录数
    limit=page_size#返回地记录数
    query=select(Book).offset(skip).limit(limit)
    result = await db.execute(query)
    books = result.scalars().all()
    return books
#图书添加接口，通过【请求体参数】实现数据库数据的添加
class BookBase(BaseModel):
    #id:str
    title:str
    author:str
    publisher:str
    price:float

@app.post("/library/books/add_book")
async def add_book(book:BookBase,db:AsyncSession=Depends(get_db)):
    book_obj=Book(**book.__dict__)#请求体参数转换成ORM对象
    db.add(book_obj)#将新书籍添加到数据库会话中
    await db.flush()#刷新会话，将新书籍插入数据库并获取生成的ID
    return {"msg":"书籍添加成功","book_id":book_obj.id}
#图书更新接口，通过【PUT+id】实现数据库数据的更新
@app.put("/library/books/update_book/{book_id}")
async def update_book(book_id:int,data:BookBase,db:AsyncSession=Depends(get_db)):
    result=await db.get(Book,book_id)#根据路径参数查询Book实例
    book_obj=result#提取Book实例
    if not book_obj:
        #return {"msg":"书籍不存在"}
        raise HTTPException(status_code=404,detail="书籍不存在")
    #更新字段
    book_obj.title=data.title
    book_obj.author=data.author
    book_obj.publisher=data.publisher
    book_obj.price=data.price
    #写入数据库
    await db.flush()#刷新会话，将更新后的书籍信息写入数据库
    return {"msg":"书籍更新成功"}
#图书删除接口，通过【DELETE+id】实现数据库数据的删除
@app.delete("/library/books/delete_book/{book_id}")
async def delete_book(book_id:int,db:AsyncSession=Depends(get_db)):
    result=await db.get(Book,book_id)#根据id在Book表中查询书籍实例
    book_obj=result#提取书籍实例
    if not book_obj:
        raise HTTPException(status_code=404,msg="书籍不存在")
    await db.delete(book_obj)
    await db.flush()#刷新会话，将删除操作写入数据库
    return {"msg":"书籍删除成功"}