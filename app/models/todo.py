from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.models.user import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func # 导入 func 来获取数据库时间
from app.db.base_class import Base


class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(255))
    completed = Column(Boolean, default=False)
    # --- 本次演练新增字段 ---
    # priority: 1代表紧急，0代表普通
    priority = Column(Integer, default=0)
    # -----------------------
    # --- 新增企业级字段 ---
    is_deleted = Column(Boolean, default=False)  # 逻辑删除标记：False 代表正常，True 代表已删
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 记录创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 每次更新时自动记录时间
    # --------------------

    owner_id = Column(Integer, ForeignKey("users.id"))