# 1. 使用轻量级 Python 基础镜像
FROM python:3.12-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 设置 Python 运行环境
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 先复制依赖文件，充分利用 Docker 构建缓存
COPY requirements.txt .

# 5. 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 6. 复制应用代码
COPY app ./app

# 7. 使用非 root 用户运行服务
RUN useradd --create-home appuser
USER appuser

# 每 30 秒检查一次应用是否能响应
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)" || exit 1

# 8. 声明应用使用的端口
EXPOSE 8000

# 9. 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]