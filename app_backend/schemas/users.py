
from pydantic import BaseModel

#这个参数在前端是请求体形式的！！
class UserRegisterRequest(BaseModel):
    username: str
    password: str