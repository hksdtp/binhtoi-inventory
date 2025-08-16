#!/bin/bash

# Script để khởi động BinhToi Inventory App với Docker
# Author: BinhToi Team

echo "🐳 Khởi động BinhToi Inventory App với Docker..."
echo "================================================"

# Kiểm tra Docker có được cài đặt không
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa được cài đặt!"
    echo "Vui lòng cài đặt Docker từ: https://docs.docker.com/get-docker/"
    exit 1
fi

# Kiểm tra Docker Compose có được cài đặt không
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose chưa được cài đặt!"
    echo "Vui lòng cài đặt Docker Compose từ: https://docs.docker.com/compose/install/"
    exit 1
fi

# Kiểm tra Docker daemon có đang chạy không
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon không chạy!"
    echo "Vui lòng khởi động Docker Desktop hoặc Docker service"
    exit 1
fi

# Kiểm tra file cần thiết
echo "🔍 Kiểm tra file cần thiết..."
required_files=("index.html" "products_data.json" "Dockerfile" "docker-compose.yml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Thiếu file: ${missing_files[*]}"
    if [[ " ${missing_files[*]} " =~ " products_data.json " ]]; then
        echo "💡 Chạy lệnh sau để tạo file dữ liệu:"
        echo "   python3 data_loader.py"
    fi
    exit 1
fi

echo "✅ Tất cả file cần thiết đã có"

# Dừng container cũ nếu có
echo "🛑 Dừng container cũ (nếu có)..."
docker-compose down 2>/dev/null

# Build và khởi động
echo "🔨 Build Docker image..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Build thất bại!"
    exit 1
fi

echo "🚀 Khởi động container..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Khởi động thất bại!"
    exit 1
fi

# Chờ container khởi động
echo "⏳ Đợi container khởi động..."
sleep 5

# Kiểm tra trạng thái
if docker-compose ps | grep -q "Up"; then
    echo "✅ Container đã khởi động thành công!"
    echo ""
    echo "🌐 Ứng dụng đang chạy tại:"
    echo "   http://localhost:8000"
    echo "   http://localhost:8000/index.html"
    echo ""
    echo "📊 Các lệnh hữu ích:"
    echo "   docker-compose logs -f          # Xem logs"
    echo "   docker-compose stop             # Dừng container"
    echo "   docker-compose restart          # Khởi động lại"
    echo "   docker-compose down             # Dừng và xóa container"
    echo ""
    
    # Tự động mở browser (macOS)
    if command -v open &> /dev/null; then
        echo "🌍 Đang mở browser..."
        open http://localhost:8000
    fi
    
else
    echo "❌ Container không khởi động được!"
    echo "📋 Logs:"
    docker-compose logs
    exit 1
fi
