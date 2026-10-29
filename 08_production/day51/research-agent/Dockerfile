FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 复制依赖清单，便于利用构建缓存
COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

# 复制应用代码
COPY app/ ./app/

# 创建非 root 用户并切换用户
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
