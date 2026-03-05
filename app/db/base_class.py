from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
@as_declarative()
class Base:
    id: Any
    __name__: str

    # 自动生成表名：把类名转成小写作为数据库表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()