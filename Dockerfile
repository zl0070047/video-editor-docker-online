FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN useradd -m -r -u 1000 appuser && \
    mkdir -p /tmp/video-editor-uploads && \
    chown -R appuser:appuser /app /tmp/video-editor-uploads && \
    chmod 755 /app && \
    chmod 1777 /tmp/video-editor-uploads

# 复制应用文件
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser app.py .
COPY --chown=appuser:appuser src/ src/
COPY --chown=appuser:appuser templates/ templates/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 切换到非 root 用户
USER appuser

# 设置环境变量
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# 暴露端口
EXPOSE ${PORT}

# 启动命令
CMD gunicorn \
    --bind 0.0.0.0:${PORT} \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --log-level debug \
    --access-logfile - \
    --error-logfile - \
    app:app 