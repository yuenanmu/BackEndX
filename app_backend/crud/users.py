from datetime import datetime, timedelta
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app_backend.models.users import User, UserToken
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
async def creat_user_token(db:AsyncSession,user_id:int):
    #生成新的令牌和过期时间
    new_token=str(uuid.uuid4())
    expires_at=datetime.now()+timedelta(days=7,hours=0,minutes=0,seconds=0)
    #查询是否已有令牌
    query_stmt=select(UserToken).where(UserToken.user_id==user_id)
    result=await db.execute(query_stmt)
    user_token=result.scalar_one_or_none()
    if user_token:#有则更新
        user_token.token=new_token
        user_token.expires_at=expires_at
    else:#无则创建,初始化UserToken对象
        new_user_token=UserToken(token=new_token,expires_at=expires_at,user_id=user_id)
        db.add(new_user_token)
        await db.commit()
    return new_token

async def authenticate_user(db:AsyncSession,username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    if not security.verify_password(password,user.password):
        return None
    return user
async def get_user_by_token(db:AsyncSession,token:str):
    #【查询令牌】是否存在且未过期
    query_stmt=select(UserToken).where(UserToken.token==token)
    result=await db.execute(query_stmt)
    user_token=result.scalar_one_or_none()
    if not user_token or user_token.expires_at<datetime.now(): #令牌不存在或者已过期
        return None
    #【查询用户信息】根据令牌关联的用户ID查询用户信息
    query_stmt=select(User).where(User.id==user_token.user_id)
    result=await db.execute(query_stmt)
    user=result.scalar_one_or_none()
    return user