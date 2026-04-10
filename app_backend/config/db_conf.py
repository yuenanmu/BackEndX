from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


#创建异步引擎
ASYNC_DATABASE_URL="mysql+aiomysql://root:173059@localhost:3306/news_app?charset=utf8"
async_engine=create_async_engine(ASYNC_DATABASE_URL,
    echo=True,#optput SQL statemens
    pool_size=5,#连接池活跃用户的大小，默认为5
    max_overflow=10#允许的额外的连接数
)
#创建异步会话工厂
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