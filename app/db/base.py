# 这里的目的是让 Base 感知到所有模型的存在
from app.db.base_class import Base  # 导入地基
from app.models.user import UserDB   # 召唤用户模型
from app.models.todo import TodoDB   # 召唤待办模型