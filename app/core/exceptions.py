from fastapi import Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# 配置日志格式和记录位置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fastapi_project.log", encoding="utf-8"), # 写入文件
        logging.StreamHandler()                    # 同时打印到终端
    ]
)
logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    # 核心：将报错的详细堆栈信息记录到日志文件
    logger.error(f"全局异常捕捉: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": 500, "msg": "服务器内部错误，请检查日志", "data": None},
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException)-> Response:
    """
    捕获手动抛出的 HTTPException (如 404, 401, 403)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError)-> Response:
    """
    捕获参数校验错误 (Pydantic 报错)
    """
    # 提取具体的报错字段名和原因
    errors = exc.errors()
    msg = f"参数校验失败: {errors[0]['loc'][-1]} {errors[0]['msg']}"
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "code": 4220,
            "message": msg,
            "data": None
        }
    )