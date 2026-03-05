from pydantic import BaseModel, Field

from datetime import datetime # 导入 datetime
from typing import Optional, List
# 创建 Todo 时，前端需要传的内容
class TodoCreate(BaseModel):
    # min_length=1 保证了必须至少有一个字符，"" 这种空字符串会被拦截
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=255)
    priority: int = 0  # 新增


# 返回给前端的 Todo 内容
class TodoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    owner_id: int

    # --- 新增：允许这两个字段展示给前端 ---
    created_at: datetime
    updated_at: Optional[datetime] = None
    # ----------------------------------
    priority: int  # 新增
    model_config = {
        "from_attributes": True
    }


# 修改任务时用的模型
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    completed: Optional[bool] = None
    priority: Optional[int] = None  # 新增
    model_config = {
        "from_attributes": True
    }