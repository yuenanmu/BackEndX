
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

#这个参数在前端是请求体形式的！！
class UserRegisterRequest(BaseModel):
    username: str
    password: str

#后端与前端交互的参数模型

class UserInfoBase(BaseModel):
    """
    用户信息基础模型
    """

    nickname:Optional[str]=Field(None,max_length=50,description="昵称")
    avatar:Optional[str]=Field(None,max_length=255,description="头像URL")
    gender:Optional[str]=Field(None,max_length=10,description="性别")
    bio:Optional[str]=Field(None,max_length=500,description="个人简介")


class UserInfoResponse(UserInfoBase):
    """
    继承了UserInfoBase,已经有nickname,avatar,gender,bio
    再加上id和username
    """
    id: int
    username:str
    #模型类配置
    model_config=ConfigDict(
        from_attributes=True#允许从ORM对象属性中取值
    )

class UserAuthResponse(BaseModel):
    token: str
    userInfo: UserInfoResponse=Field(...,alias="userInfo")
    #模型类配置，允许从ORM对象创建模型实例
    model_config=ConfigDict(
        populate_by_name=True,#alias/字段名 兼容？
        from_attributes=True#允许从ORM对象属性中取值
    )
class UserUpdatePasswordRequest(BaseModel):
    old_password:str=Field(...,alias="oldPassword")
    new_password:str=Field(...,min_length=6,alias="newPassword")#最少6位密码