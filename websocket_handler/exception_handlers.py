from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import BaseModel
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TranscriptionResponse(BaseModel):
    """
    语音识别响应模型
    
    属性:
        code (int): 响应状态码,0表示成功
        msg (str): 响应消息,如"streaming"表示正在流式传输,"complete"表示传输完成
        data (str): 响应数据,包含语音识别的文本结果或语言模型生成的文本
    """
    code: int
    msg: str
    data: str

async def custom_exception_handler(request: Request, exc: Exception):
    """
    自定义异常处理函数
    
    参数:
        request (Request): FastAPI请求对象
        exc (Exception): 异常对象
    
    返回:
        JSONResponse: JSON格式的错误响应
    """
    logger.error("发生异常", exc_info=True)
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail
        data = ""
    elif isinstance(exc, RequestValidationError):
        status_code = HTTP_422_UNPROCESSABLE_ENTITY
        message = "验证错误: " + str(exc.errors())
        data = ""
    else:
        status_code = 500
        message = "内部服务器错误: " + str(exc)
        data = ""

    return JSONResponse(
        status_code=status_code,
        content=TranscriptionResponse(
            code=status_code,
            msg=message,
            data=data
        ).model_dump()
    )