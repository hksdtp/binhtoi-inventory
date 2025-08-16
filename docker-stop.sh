#!/bin/bash

# Script để dừng BinhToi Inventory App Docker container
# Author: BinhToi Team

echo "🛑 Dừng BinhToi Inventory App Docker container..."
echo "================================================"

# Kiểm tra container có đang chạy không
if docker-compose ps | grep -q "Up"; then
    echo "📋 Container đang chạy, tiến hành dừng..."
    
    # Dừng container
    docker-compose stop
    
    if [ $? -eq 0 ]; then
        echo "✅ Container đã dừng thành công!"
    else
        echo "❌ Có lỗi khi dừng container"
        exit 1
    fi
else
    echo "ℹ️  Container không đang chạy"
fi

# Hỏi có muốn xóa container không
echo ""
read -p "🗑️  Bạn có muốn xóa container và volumes không? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Đang xóa container và volumes..."
    docker-compose down -v
    
    if [ $? -eq 0 ]; then
        echo "✅ Đã xóa container và volumes thành công!"
    else
        echo "❌ Có lỗi khi xóa container"
        exit 1
    fi
else
    echo "ℹ️  Giữ nguyên container (đã dừng)"
fi

echo ""
echo "📊 Các lệnh hữu ích:"
echo "   ./docker-start.sh               # Khởi động lại"
echo "   docker-compose up -d            # Khởi động container đã có"
echo "   docker-compose logs -f          # Xem logs"
echo "   docker system prune             # Dọn dẹp Docker system"
echo ""
echo "👋 Hoàn tất!"
