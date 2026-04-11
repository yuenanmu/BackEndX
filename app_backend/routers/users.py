from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.config.db_conf import get_db
from app_backend.schemas.users import UserRegisterRequest
from app_backend.crud import users
router=APIRouter(prefix="/api/users",tags=["用户相关接口"])

@router.post("/register")
async def register(user_data: UserRegisterRequest, db:AsyncSession=Depends(get_db)):#用户信息 (需要数据校验)和db
    #查询用户是否存在,如果存在，抛出异常
    exsiting_user=await users.get_user_by_username(db,user_data.username)
    if exsiting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    #创建新用户
    new_user=await users.create_user(db,user_data)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": new_user.id,
                "username": new_user.username,
                "bio": new_user.bio,
                "avatar": new_user.avatar,
            }
        }
    }