#!/bin/bash

echo "🚀 Pushing code to GitHub..."

# Kiểm tra xem repository đã được tạo chưa
echo "📋 Đảm bảo bạn đã tạo repository 'binhtoi-inventory' trên GitHub"
echo "   URL: https://github.com/new"
echo "   Name: binhtoi-inventory"
echo "   Description: 🏪 Modern Inventory Management System with Supabase Integration"
echo ""

read -p "Đã tạo repository trên GitHub? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Vui lòng tạo repository trước và chạy lại script"
    exit 1
fi

# Remove existing remote (nếu có)
git remote remove origin 2>/dev/null || true

# Add remote
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/hksdtp/binhtoi-inventory.git

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Code đã được push lên GitHub"
    echo "🔗 Repository URL: https://github.com/hksdtp/binhtoi-inventory"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Mở repository trên GitHub"
    echo "   2. Thêm README badges nếu muốn"
    echo "   3. Setup GitHub Pages (nếu muốn demo online)"
else
    echo ""
    echo "❌ ERROR: Không thể push lên GitHub"
    echo "💡 Kiểm tra:"
    echo "   1. Repository đã được tạo chưa?"
    echo "   2. Tên repository có đúng không?"
    echo "   3. Có quyền truy cập không?"
fi
