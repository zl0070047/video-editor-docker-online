FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 复制应用文件
COPY requirements.txt .
COPY app.py .
COPY src/ src/
COPY templates/ templates/

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建上传目录
RUN mkdir -p /tmp/video-editor-uploads && chmod 777 /tmp/video-editor-uploads

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000

# 暴露端口（Render 会自动设置实际端口）
EXPOSE 10000

# 启动命令
CMD gunicorn --bind 0.0.0.0:$PORT app:app 