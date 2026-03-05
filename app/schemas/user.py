from pydantic import BaseModel, Field

# 注册时用的模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    password: str = Field(..., min_length=8)

# 返回给前端的用户信息（不带密码）
class UserOut(BaseModel):
    id: int
    username: str

    model_config = {
        "from_attributes": True  # 依然是这个固定字符串
    }