from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.config.db_conf import get_db
from app_backend.schemas.users import UserRegisterRequest
router=APIRouter(prefix="/api/users",tags=["用户相关接口"])

@router.post("/register")
async def register(user_data: UserRegisterRequest, db:AsyncSession=Depends(get_db)):#用户信息 (需要数据校验)和db
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": "用户访问令牌",
            "userInfo": {
                "id": 1,
                "username": user_data.username,
                "bio": "这个人很懒，什么都没留下",
                "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
            }
        }
    }