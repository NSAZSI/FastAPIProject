# 1. 强制指定 bookworm 地基
FROM python:3.11-slim-bookworm

# 2. 设置工作目录
WORKDIR /app

# --- 核心修复：直接修改新版的 .sources 文件，解决文件不存在的问题 ---
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# 3. 环境变量
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 安装系统依赖（现在路径对齐了，可以起飞了）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. 复制依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 复制源码
COPY . .

# 7. 暴露端口
EXPOSE 8888

# 8. 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]