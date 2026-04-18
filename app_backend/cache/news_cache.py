from typing import Any, Dict, List

from app_backend.config.cache_config import get_json_cache
from app_backend.config.cache_config import set_cache

CATEGORIES_KEY="news:categories"
NEWS_LIST_KEY="news:list"
#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIES_KEY)
#写入新闻分类缓存：缓存数据，过期时间
#分类，配置：7200，2h;列表：600，10min;详情：1800，30min；验证码：120--数据越稳定，缓存越持久
#避免所有key同时过期，引起缓存雪崩
async def set_cache_categories(data:List[Dict[str,Any]],expire:int=7200):
    return await set_cache(CATEGORIES_KEY,data,expire)

async def get_cached_news_list(category_id:int,page:int,page_size:int,expire:int=600):
    category_id=category_id if category_id is not None else "all"
    key=f"{NEWS_LIST_KEY}:{category_id}:{page}:{page_size}"
    return await get_json_cache(key)
async def set_cache_news_list(category_id:int,page:int,page_size:int,data:List[Dict[str,Any]],expire:int=600):
    category_id=category_id if category_id is not None else "all"
    key=f"{NEWS_LIST_KEY}:{category_id}:{page}:{page_size}"
    return await set_cache(key,data,expire)