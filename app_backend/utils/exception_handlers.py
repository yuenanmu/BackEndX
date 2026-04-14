from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError#来自 ORM 框架 SQLAlchemy，它是 ORM 层面的异常
from app_backend.utils.exception import (
    http_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
    general_exception_handler
)
def register_exception_handlers(app):
    """
    全局注册异常处理器：子类在前父类在后，从具体到模糊顺序注册
    """
    app.add_exception_handler(HTTPException,http_exception_handler)
    app.add_exception_handler(IntegrityError,integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)
    app.add_exception_handler(Exception,general_exception_handler)