import json
from typing import Any

import redis.asyncio  as redis

REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
redis_client=redis.Redis(
    host=REDIS_HOST,#连接redis服务器的地址
    port=REDIS_PORT,#连接redis服务器的端口
    db=REDIS_DB,#连接redis服务器的数据库索引，默认为0，共16个：0~15
    decode_responses=True#将redis返回的字节数据解码为字符串，默认为False，如果为True，则返回字符串类型的数据
)


#设置和读取（字符串 和 字典）
async def  set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,dict):
            #转字符串再存
            value=json.dumps(value,ensure_ascii=False)
        await redis_client.set(key,expire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
    
async def get_cache(key:str):
    try:
        data=await redis_client.get(key)
        return data
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None
    
async def get_json_cache(key:str):
    try:
        data=await redis_client.get(key)
        if data:
            return json.loads(data)#序列化
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")
        return None
