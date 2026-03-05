from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1. 定义数据库配置
    DATABASE_URL: str

    # 2. 定义 JWT 配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # 给定默认值
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 3. 项目基本信息
    PROJECT_NAME: str = "Todo Project"

    # 4. 配置读取 .env 文件的规则
    model_config = SettingsConfigDict(
        env_file=".env",  # 告诉它读取根目录下的 .env
        env_file_encoding="utf-8",  # 防止中文乱码
        case_sensitive=True  # 变量名区分大小写
    )


# 实例化，全局直接调用 settings 即可
settings = Settings()