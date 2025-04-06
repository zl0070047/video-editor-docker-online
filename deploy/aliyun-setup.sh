#!/bin/bash

# 更新系统
sudo apt-get update
sudo apt-get upgrade -y

# 安装必要的系统工具
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    nginx

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 创建应用目录
sudo mkdir -p /app/video-editor
sudo mkdir -p /app/video-editor/data

# 配置 Nginx
sudo tee /etc/nginx/sites-available/video-editor <<EOF
server {
    listen 80;
    server_name \$host;

    client_max_body_size 16M;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 启用网站配置
sudo ln -s /etc/nginx/sites-available/video-editor /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx

# 创建清理脚本
sudo tee /app/video-editor/cleanup.sh <<EOF
#!/bin/bash
find /tmp/video-editor-uploads -type f -mtime +1 -delete
EOF

sudo chmod +x /app/video-editor/cleanup.sh

# 添加定时任务清理临时文件
(crontab -l 2>/dev/null; echo "0 0 * * * /app/video-editor/cleanup.sh") | crontab - 