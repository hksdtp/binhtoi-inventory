# 🎨 Binhtoi Inventory Management System - Pinterest Style

> Modern inventory management system with Pinterest-inspired design, Supabase integration, and mobile-first experience

[![GitHub stars](https://img.shields.io/github/stars/hksdtp/binhtoi-inventory?style=social)](https://github.com/hksdtp/binhtoi-inventory/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/hksdtp/binhtoi-inventory?style=social)](https://github.com/hksdtp/binhtoi-inventory/network/members)
[![GitHub issues](https://img.shields.io/github/issues/hksdtp/binhtoi-inventory)](https://github.com/hksdtp/binhtoi-inventory/issues)
[![License](https://img.shields.io/github/license/hksdtp/binhtoi-inventory)](LICENSE)

A comprehensive inventory management system featuring **Pinterest-style masonry layout**, mobile-first design optimized for iOS experience, real-time data synchronization with Supabase, and advanced image management capabilities.

## ✨ Features

### 🎨 Pinterest-Style Design
- 📱 **Masonry Grid Layout** - Variable height cards with natural stacking
- 🔄 **Infinite Scroll** - Smooth loading as you scroll down
- 🎭 **Hover Overlays** - Interactive action buttons on card hover
- 📲 **Pull-to-Refresh** - iOS-style refresh functionality
- 🎯 **Floating Action Button** - Quick access to upload features
- 📱 **Mobile-First** - Optimized for Pinterest iOS app experience

### 🎯 Core Features
- 📱 **Responsive Design** - 2-6 columns based on screen size
- 🔍 **Smart Search** - Real-time product search and filtering
- 📊 **Product Details** - Modal overlays with full information
- 🏷️ **Category Management** - Organize products by categories
- 📈 **Stock Tracking** - Monitor inventory levels and stock status

### 🖼️ Image Management
- 📤 **Bulk Upload** - Upload multiple product images at once
- 🌐 **Web Upload Interface** - Drag-and-drop image upload from browser
- ☁️ **Cloud Storage** - Images stored on Supabase Storage with CDN
- 🖼️ **Auto Optimization** - Automatic image processing and optimization
- 📱 **Mobile Upload** - Touch-friendly upload experience

### 🔄 Data Synchronization
- ⚡ **Real-time Sync** - Instant data synchronization with Supabase
- 🔄 **Offline Support** - Works offline with local caching
- 📱 **Cross-device Sync** - Access your data from any device
- 🔐 **Secure Backup** - Automatic cloud backup and recovery

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python with Supabase client
- **Database**: PostgreSQL (Supabase)
- **Storage**: Supabase Storage with CDN
- **Styling**: Tailwind CSS
- **Icons**: Font Awesome
- **Image Processing**: Pillow (PIL)

## 📁 Project Structure

```bash
binhtoi-inventory/
├── 📄 index.html              # Main web interface
├── 🐍 supabase_config.py      # Database configuration
├── 📤 upload_images.py        # Bulk image upload script
├── 🎨 create_sample_images.py # Generate sample images
├── 🔄 supabase_sync.py        # Data synchronization
├── 📊 products_data.json      # Local product data
├── 🖼️ images/                 # Product images folder
├── 📚 SUPABASE_SETUP.md       # Setup instructions
├── 📖 HUONG_DAN_HINH_ANH.md   # Image management guide
└── ⚙️ requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/hksdtp/binhtoi-inventory.git
   cd binhtoi-inventory
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Setup Supabase** (Optional - for cloud features)
   ```bash
   # Copy environment template
   cp .env.example .env

   # Edit .env with your Supabase credentials
   # Get them from: https://supabase.com/dashboard
   ```

4. **Run the application**
   ```bash
   # Start the web server
   python3 -m http.server 8001

   # Open in browser
   open http://localhost:8001
   ```

### With Supabase Integration

1. **Sync data to cloud**
   ```bash
   python3 supabase_sync.py
   ```

2. **Upload product images**
   ```bash
   # Place images in images/ folder (named by SKU)
   python3 upload_images.py
   ```

## 📊 Dữ liệu hiện tại

Từ file "Ton kho binh.xlsx" (01/08/2025 - 07/08/2025):
- **32 sản phẩm** được tích hợp
- **2,602 tổng tồn kho**
- **3 danh mục chính**:
  - Bình xông đốt tinh dầu: 18 sản phẩm (1,425 tồn)
  - Bình để nến: 9 sản phẩm (726 tồn)  
  - Cốc nến thơm: 5 sản phẩm (451 tồn)

## 🎯 Tính năng nổi bật

### Dashboard thông minh
- **Tổng SP**: Hiển thị tổng số sản phẩm
- **Tổng tồn**: Tổng số lượng tồn kho
- **Sắp hết**: Số sản phẩm có tồn ≤ 10

### Hệ thống màu sắc tồn kho
- 🔴 **Đỏ**: Tồn ≤ 10 (sắp hết)
- 🟡 **Vàng**: Tồn 11-50 (trung bình)
- 🟢 **Xanh**: Tồn > 50 (nhiều)

### Tìm kiếm & Lọc
- Tìm theo tên sản phẩm
- Tìm theo mã SKU
- Lọc theo danh mục
- Kết hợp tìm kiếm + lọc

## 🔧 Tùy chỉnh

### Cập nhật dữ liệu mới
1. Thay thế file `Ton kho binh.xlsx` bằng file mới
2. Chạy lại: `python3 data_loader.py`
3. Refresh app trong browser

### Thêm danh mục mới
Chỉnh sửa trong `index.html` tại phần:
```html
<select id="productCategory">
    <option value="Bình để nến">Bình để nến</option>
    <option value="Bình xông đốt tinh dầu">Bình xông đốt tinh dầu</option>
    <option value="Cốc nến thơm">Cốc nến thơm</option>
    <option value="Danh mục mới">Danh mục mới</option>
</select>
```

### Thay đổi port server
```bash
# Sử dụng port khác nếu 8000 bị chiếm
python3 -m http.server 8080
```

## 🎨 Giao diện

- **Header**: Tìm kiếm + filter danh mục
- **Stats Cards**: 3 thẻ thống kê nhanh
- **Product Grid**: Lưới sản phẩm 2 cột
- **Bottom Nav**: 5 tab điều hướng
- **Modal**: Chi tiết/chỉnh sửa sản phẩm

## 📱 Responsive Design

- **Mobile First**: Tối ưu cho điện thoại
- **Tablet**: Tự động điều chỉnh layout
- **Desktop**: Hiển thị tốt trên màn hình lớn
- **Safe Area**: Hỗ trợ iPhone notch

## 🔄 Cập nhật định kỳ

Để cập nhật dữ liệu tồn kho hàng tuần:
1. Export file Excel mới từ hệ thống
2. Đặt tên file: `Ton kho binh.xlsx`
3. Chạy: `python3 data_loader.py`
4. App sẽ tự động load dữ liệu mới

## 🐛 Troubleshooting

### Lỗi "File not found"
- Kiểm tra file `Ton kho binh.xlsx` có tồn tại
- Chạy lại `python3 data_loader.py`

### Port đã được sử dụng
```bash
# Thử port khác
python3 server.py
# Hoặc
python3 -m http.server 8001
```

### Dữ liệu không hiển thị
- Kiểm tra file `products_data.json` có được tạo
- Mở Developer Tools (F12) để xem lỗi console
- Refresh browser (Ctrl+R)

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Python 3.x đã được cài đặt
2. File Excel có đúng format
3. Browser hỗ trợ JavaScript
4. Không có firewall chặn port 8000
