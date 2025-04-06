# 在线视频编辑器

一个简单的在线视频编辑器，支持视频剪辑和格式转换。使用 Flask 和 MoviePy 构建，部署在 Render 平台上。

## 功能特点

- 支持上传视频文件（MP4、AVI、MOV、MKV）
- 在线预览视频
- 设置视频剪辑起止时间
- 支持多种输出格式（MP4、AVI、MOV、GIF）
- 在线处理和下载

## 技术栈

- 后端：Flask + MoviePy
- 前端：Bootstrap + 原生 JavaScript
- 容器化：Docker
- 部署平台：Render

## 本地开发

1. 克隆仓库：
```bash
git clone https://github.com/zl0070047/video-editor-docker-online.git
cd video-editor-docker-online
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python app.py
```

## Docker 部署

```bash
docker-compose up -d
```

## 使用说明

1. 打开应用网页
2. 点击"选择文件"上传视频
3. 设置剪辑起止时间
4. 选择输出格式
5. 点击"处理视频"
6. 等待处理完成后自动下载

## 注意事项

- 上传文件大小限制为 16MB
- 支持的视频格式：MP4、AVI、MOV、MKV
- 支持的输出格式：MP4、AVI、MOV、GIF

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 