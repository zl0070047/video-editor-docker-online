# 在线视频编辑器

一个简单的在线视频编辑器，支持视频剪辑和格式转换。

## 功能特点

- 支持上传视频文件（MP4、AVI、MOV、MKV）
- 在线预览视频
- 设置视频剪辑起止时间
- 支持多种输出格式（MP4、AVI、MOV、GIF）
- 在线处理和下载

## 部署说明

### 使用 Docker Compose 部署（推荐）

1. 克隆仓库：
```bash
git clone https://github.com/zl0070047/video-editor-docker.git
cd video-editor-docker
```

2. 修改配置：
- 在 `docker-compose.yml` 中修改 `SECRET_KEY` 环境变量
- 根据需要修改端口映射（默认 5000）

3. 启动服务：
```bash
docker-compose up -d
```

服务将在 http://localhost:5000 运行

### 手动部署

1. 安装系统依赖：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip ffmpeg

# CentOS/RHEL
sudo yum install -y python3 python3-pip ffmpeg
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务：
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## 使用说明

1. 打开浏览器访问 http://localhost:5000
2. 点击"选择文件"上传视频
3. 设置剪辑起止时间
4. 选择输出格式
5. 点击"处理视频"
6. 等待处理完成后自动下载

## 注意事项

- 上传文件大小限制为 16MB
- 临时文件存储在 /tmp/video-editor-uploads 目录
- 建议定期清理临时文件

## 技术栈

- 后端：Flask + MoviePy
- 前端：Bootstrap + 原生 JavaScript
- 容器化：Docker + Docker Compose

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 