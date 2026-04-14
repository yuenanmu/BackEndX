from fastapi import Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app_backend.config.db_conf import get_db
from app_backend.crud import users


async def get_current_user(
        authorization:str=Header(...,alias="Authorization"),
        db:AsyncSession=Depends(get_db),
):
    token=authorization.split(" ")[0]
    current_user=await users.get_user_by_token(db,token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌")
    return current_user
