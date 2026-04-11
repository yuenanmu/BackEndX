from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_backend.models.users import User
from app_backend.schemas.users import UserRegisterRequest
from app_backend.utils import security

async def get_user_by_username(db: AsyncSession, username: str):
    query_stmt = select(User).where(User.username == username)
    result = await db.execute(query_stmt)
    return result.scalar_one_or_none()

#数据库增加操作-创建用户
async def create_user(db:AsyncSession,user_data:UserRegisterRequest):
    #先加密
    print(f"加密前的密码长度：{len(user_data.password)}")
    hashed_password=security.get_hash_password(user_data.password)
    print(f"加密后的密码长度: {len(hashed_password)}")
    new_user=User(username=user_data.username,password=hashed_password)#创建一个User对象，包含了用户名和加密后的密码
    #在 SQLAlchemy 异步会话中，add()、delete() 等方法仍然是同步的，
    #只有真正涉及数据库通信的方法（如 execute(), commit(), refresh(), flush()）才是异步的。
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)#刷新User对象状态，获取数据库生成的ID等信息
    return new_user