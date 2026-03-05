from pydantic import BaseModel
from typing import Any, Optional

class UnifiedResponse(BaseModel):
    success: bool      # 操作是否成功
    code: int          # 自定义业务状态码（非 HTTP 状态码）
    message: str       # 错误提示信息
    data: Optional[Any] = None # 成功时返回的数据