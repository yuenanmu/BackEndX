from fastapi import APIRouter

#创建一个APIRouter实例，设置前缀prefix和标签tags
router=APIRouter(prefix="/api/news",tags=["新闻相关接口"])
#接口实现流程
#1.模块化路由
#2.设计模型类
#3.crud中实现增删改查方法
#4.在路由处理函数中调用crud函数实现接口功能



@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 10):
    return {"code":200,"message":"这是新闻分类接口", "skip": skip, "limit": limit}