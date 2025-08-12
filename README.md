# 📱 App Quản Lý Tồn Kho Bình

Ứng dụng web quản lý tồn kho với giao diện mobile-first, được xây dựng dựa trên dữ liệu thực từ file Excel "Ton kho binh.xlsx".

## 🚀 Tính năng chính

- **📊 Dashboard tổng quan**: Hiển thị tổng số sản phẩm, tổng tồn kho, số sản phẩm sắp hết hàng
- **🔍 Tìm kiếm thông minh**: Tìm theo tên sản phẩm, mã SKU, hoặc danh mục
- **🏷️ Lọc theo danh mục**: Bình để nến, Bình xông đốt tinh dầu, Cốc nến thơm
- **📱 Giao diện responsive**: Tối ưu cho mobile và desktop
- **🎨 UI/UX hiện đại**: Thiết kế theo phong cách Shopee với animations mượt mà
- **⚡ Hiệu suất cao**: Load dữ liệu nhanh với lazy loading

## 📁 Cấu trúc dự án

```
binhtoi/
├── Ton kho binh.xlsx      # File Excel nguồn
├── data_loader.py         # Script đọc Excel và chuyển đổi JSON
├── products_data.json     # Dữ liệu sản phẩm (được tạo tự động)
├── index.html            # App chính
├── server.py             # HTTP server
├── giaodienapp           # File giao diện mẫu gốc
└── README.md             # Hướng dẫn này
```

## 🛠️ Cách chạy

### 1. Chuẩn bị dữ liệu
```bash
# Đọc file Excel và tạo JSON
python3 data_loader.py
```

### 2. Chạy server
```bash
# Khởi động server web
python3 server.py
```

### 3. Mở app
- Server sẽ tự động mở browser tại: `http://localhost:8000/index.html`
- Hoặc mở thủ công: http://localhost:8000/index.html

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
