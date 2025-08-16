#!/bin/bash

# Script để khởi động BinhToi Inventory App
# Hỗ trợ cả Docker và Python trực tiếp

echo "🚀 BinhToi Inventory App Launcher"
echo "=================================="

# Kiểm tra file cần thiết
echo "🔍 Kiểm tra file cần thiết..."
required_files=("index.html" "products_data.json" "server.py")
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

# Hỏi user muốn chạy bằng cách nào
echo ""
echo "Chọn cách khởi động:"
echo "1) Python trực tiếp (đơn giản, nhanh)"
echo "2) Docker (cần Docker Desktop)"
echo ""
read -p "Nhập lựa chọn (1 hoặc 2): " choice

case $choice in
    1)
        echo "🐍 Khởi động với Python..."
        
        # Kiểm tra Python
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python3 chưa được cài đặt!"
            exit 1
        fi
        
        # Kiểm tra port 8000
        if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
            echo "⚠️  Port 8000 đang được sử dụng"
            echo "🛑 Dừng process cũ..."
            kill $(lsof -ti:8000) 2>/dev/null || true
            sleep 2
        fi
        
        echo "🌐 Khởi động server tại http://localhost:8000"
        python3 server.py
        ;;
        
    2)
        echo "🐳 Khởi động với Docker..."
        
        # Kiểm tra Docker
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker chưa được cài đặt!"
            echo "Tải Docker Desktop từ: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        # Kiểm tra Docker daemon
        if ! docker info &> /dev/null; then
            echo "❌ Docker daemon không chạy!"
            echo "Vui lòng khởi động Docker Desktop"
            exit 1
        fi
        
        # Dừng container cũ
        echo "🛑 Dừng container cũ (nếu có)..."
        docker-compose down 2>/dev/null || true
        
        # Khởi động
        echo "🚀 Khởi động Docker container..."
        docker-compose up -d
        
        if [ $? -eq 0 ]; then
            echo "✅ Container đã khởi động thành công!"
            echo "🌐 Ứng dụng đang chạy tại: http://localhost:8000"
            
            # Hiển thị logs
            echo ""
            echo "📋 Logs (Ctrl+C để thoát):"
            docker-compose logs -f
        else
            echo "❌ Khởi động Docker thất bại!"
            echo "💡 Thử chạy với Python: ./start-app.sh và chọn option 1"
            exit 1
        fi
        ;;
        
    *)
        echo "❌ Lựa chọn không hợp lệ!"
        exit 1
        ;;
esac
