# Personal Todo Logic Isolation System (基于 FastAPI 的多租户待办系统)

本项目是一个专为高并发、安全性设计的个人任务管理系统后端。它不仅实现了基础的 CRUD 功能，还深度集成了 **JWT 鉴权**、**多租户数据隔离**、**数据库版本管理**以及**异步日志系统**。

## 🚀 项目核心亮点

- **多租户数据隔离**：通过依赖注入机制，在数据库查询层面强制绑定 `owner_id`，从根源杜绝越权访问漏洞。
    
- **异步架构 (Async)**：全栈采用 `FastAPI` + `SQLAlchemy 2.0` 异步模式，大幅提升 IO 密集型场景下的系统响应速度。
    
- **平滑升级 (Alembic)**：集成 Alembic 实现数据库版本控制，支持生产环境下的零停机表结构变更。
    
- **工程化异常处理**：自研全局异常拦截器，实现统一的 JSON 响应格式，并自动记录详细堆栈至 `.log` 文件。
    

## 🛠️ 技术栈

- **框架**: FastAPI (Python 3.10+)
    
- **数据库**: MySQL 8.0
    
- **ORM**: SQLAlchemy 2.0 (Async)
    
- **鉴权**: Jose (JWT), Passlib (Bcrypt)
    
- **迁移**: Alembic
    
- **日志**: Standard Logging with FileHandler
    

## 📦 快速开始

### 1. 环境准备

Bash

```
# 克隆项目
git clone https://github.com/your-username/FastAPIProject.git
cd FastAPIProject

# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
```

### 2. 安装依赖

Bash

```
pip install -r requirements.txt
```

### 3. 环境配置

在根目录下创建 `.env` 文件，并参照以下格式配置：

Ini, TOML

```
DATABASE_URL=mysql+asyncmy://root:你的密码@localhost:3306/你的数据库名
SECRET_KEY=你的随机密钥
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. 数据库初始化 (Alembic)

本项目使用 Alembic 管理表结构，启动前请执行迁移命令：

Bash

```
alembic upgrade head
```

### 5. 启动服务

Bash

```
python main.py
```

访问地址：`http://127.0.0.1:8888/docs` 进入 Swagger UI 进行交互测试。
