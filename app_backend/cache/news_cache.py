from typing import Any, Dict, List

from app_backend.config.cache_config import get_json_cache
from app_backend.config.cache_config import set_cache

CATEGORIES_KEY="news:categories"
#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)
#写入新闻分类缓存：缓存数据，过期时间
#分类，配置：7200，2h;列表：600，10min;详情：1800，30min；验证码：120--数据越稳定，缓存越持久
#避免所有key同时过期，引起缓存雪崩
async def set_cache_categories(data:List[Dict[str,Any]],expire:int=7200):
    return await set_cache(CATEGORIES_KEY,data,expire)