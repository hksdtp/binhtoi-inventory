# 🐳 Docker Guide - BinhToi Inventory App

## 📋 Tổng quan

BinhToi Inventory App hỗ trợ chạy bằng Docker để đảm bảo môi trường nhất quán và dễ dàng triển khai.

## 🚀 Cách khởi động nhanh

### Option 1: Script tự động (Khuyến nghị)
```bash
./start-app.sh
# Chọn option 2 cho Docker
```

### Option 2: Docker Compose trực tiếp
```bash
# Khởi động
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

### Option 3: Docker commands thủ công
```bash
# Build image
docker build -t binhtoi-inventory .

# Chạy container
docker run -d -p 8000:8000 --name binhtoi-app binhtoi-inventory

# Dừng container
docker stop binhtoi-app
docker rm binhtoi-app
```

## 📁 Cấu trúc Docker

### Dockerfile
- **Base image**: `python:3.11-slim`
- **Security**: Non-root user (appuser)
- **Port**: 8000
- **Working directory**: `/app`

### docker-compose.yml
- **Service name**: `binhtoi-webapp`
- **Container name**: `binhtoi-inventory`
- **Port mapping**: `8000:8000`
- **Volume mount**: Current directory → `/app`
- **Health check**: HTTP check mỗi 30s

### .dockerignore
Loại trừ các file không cần thiết:
- Git files
- Python cache
- IDE files
- Documentation
- Temporary files

## 🛠️ Yêu cầu hệ thống

### Docker Desktop
- **macOS**: [Download Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/)
- **Windows**: [Download Docker Desktop for Windows](https://docs.docker.com/desktop/windows/install/)
- **Linux**: [Install Docker Engine](https://docs.docker.com/engine/install/)

### Kiểm tra cài đặt
```bash
# Kiểm tra Docker
docker --version
docker-compose --version

# Kiểm tra Docker daemon
docker info
```

## 🔧 Scripts hỗ trợ

### docker-start.sh
Script khởi động tự động với kiểm tra đầy đủ:
- ✅ Kiểm tra Docker installation
- ✅ Kiểm tra file cần thiết
- ✅ Build và start container
- ✅ Health check
- ✅ Tự động mở browser

### docker-stop.sh
Script dừng container an toàn:
- 🛑 Dừng container
- 🗑️ Tùy chọn xóa container và volumes
- 📋 Hiển thị commands hữu ích

### start-app.sh
Script universal launcher:
- 🐍 Option 1: Python trực tiếp
- 🐳 Option 2: Docker container

## 📊 Monitoring và Debugging

### Xem logs
```bash
# Logs realtime
docker-compose logs -f

# Logs của service cụ thể
docker-compose logs binhtoi-webapp

# Logs với timestamp
docker-compose logs -t
```

### Kiểm tra container
```bash
# Danh sách containers
docker-compose ps

# Thông tin chi tiết
docker inspect binhtoi-inventory

# Resource usage
docker stats binhtoi-inventory
```

### Truy cập container
```bash
# Shell vào container
docker-compose exec binhtoi-webapp bash

# Chạy command trong container
docker-compose exec binhtoi-webapp ls -la
```

## 🔄 Development Workflow

### Hot reload
Volume mount cho phép thay đổi code realtime:
```bash
# File thay đổi sẽ được sync ngay lập tức
# Không cần rebuild image cho code changes
```

### Rebuild khi cần
```bash
# Rebuild image sau khi thay đổi Dockerfile hoặc requirements
docker-compose build

# Force rebuild
docker-compose build --no-cache
```

## 🚨 Troubleshooting

### Port đã được sử dụng
```bash
# Tìm process sử dụng port 8000
lsof -ti:8000

# Kill process
kill $(lsof -ti:8000)

# Hoặc thay đổi port trong docker-compose.yml
ports:
  - "8001:8000"  # Host port 8001
```

### Docker daemon không chạy
```bash
# macOS/Windows: Khởi động Docker Desktop
# Linux: 
sudo systemctl start docker
```

### Permission denied
```bash
# Thêm user vào docker group (Linux)
sudo usermod -aG docker $USER
# Logout và login lại
```

### Container không start
```bash
# Xem logs chi tiết
docker-compose logs

# Kiểm tra health check
docker-compose ps
```

## 🌐 Truy cập ứng dụng

Sau khi khởi động thành công:
- **URL**: http://localhost:8000
- **Direct**: http://localhost:8000/index.html

## 🧹 Cleanup

### Dọn dẹp project
```bash
# Dừng và xóa containers
docker-compose down -v

# Xóa images
docker rmi binhtoi-binhtoi-webapp
```

### Dọn dẹp Docker system
```bash
# Xóa unused containers, networks, images
docker system prune

# Xóa tất cả (cẩn thận!)
docker system prune -a
```

## 📈 Production Deployment

### Environment variables
```yaml
environment:
  - NODE_ENV=production
  - PORT=8000
  - DEBUG=false
```

### Resource limits
```yaml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
```

### Health checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🎯 Best Practices

1. **Always use .dockerignore** để giảm build context
2. **Multi-stage builds** cho production
3. **Non-root user** cho security
4. **Health checks** cho monitoring
5. **Volume mounts** cho development
6. **Environment variables** cho configuration

---

## 📞 Support

Nếu gặp vấn đề với Docker:
1. Kiểm tra Docker Desktop đã chạy
2. Xem logs: `docker-compose logs`
3. Thử restart: `docker-compose restart`
4. Fallback: Sử dụng Python trực tiếp với `./start-app.sh`
