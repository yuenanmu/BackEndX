from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app_backend.config.db_conf import get_db
from app_backend.schemas.users import UserAuthResponse, UserInfoResponse, UserRegisterRequest
from app_backend.crud import users
from app_backend.utils.response import success_response
from app_backend.utils.auth import get_current_user
router=APIRouter(prefix="/api/user",tags=["用户相关接口"])

@router.post("/register")
async def register(user_data: UserRegisterRequest, db:AsyncSession=Depends(get_db)):#用户信息 (需要数据校验)和db

    #查询用户是否存在,如果存在，抛出异常
    exsiting_user=await users.get_user_by_username(db,user_data.username)
    if exsiting_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    #创建新用户
    new_user=await users.create_user(db,user_data)
    new_user_token=await users.creat_user_token(db,new_user.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": new_user_token,
    #         "userInfo": {
    #             "id": new_user.id,
    #             "username": new_user.username,
    #             "bio": new_user.bio,
    #             "avatar": new_user.avatar,
    #         }
    #     }
    # }
    response_data=UserAuthResponse(token=new_user_token,userInfo=UserInfoResponse.model_validate(new_user))
    return success_response(message="注册成功",data=response_data)

@router.post("/login")
async def login(user_data: UserRegisterRequest, db:AsyncSession=Depends(get_db)):
    #查询是否存在->密码是否正确->创建token->返回token和用户信息
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:#虽然有全局异常处理，但是这里还是需要处理一下，不然会返回500错误，而不是401错误
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    user_token=await users.creat_user_token(db,user.id)
    response_data=UserAuthResponse(token=user_token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)

@router.get("/info")
async def get_user_info(current_user=Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(current_user))