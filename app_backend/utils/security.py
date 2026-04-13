from passlib.context import CryptContext

#创建密码上下文：就是加密算法解释器
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

# #密码加密
def get_hash_password(password: str) -> str:
    # 1. 直接对【字符串】截断，不转 bytes！
    # 2. 安全截断：保证不超过 72 字节
    encoded = password.encode("utf-8")
    if len(encoded) > 72:
        encoded = encoded[:72]
    safe_password = encoded.decode("utf-8", "ignore")  # 转回字符串

    # 3. 只传字符串！绝对不传 bytes！
    return pwd_context.hash(safe_password)  # ✅ ✅ ✅    
    

#密码验证
def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)