# Hướng Dẫn Quản Lý Hình Ảnh Sản Phẩm

## 🎯 Tổng Quan

Dự án đã được tích hợp hoàn toàn với **Supabase Storage** để quản lý hình ảnh sản phẩm một cách chuyên nghiệp với các tính năng:

- ✅ **Upload hình ảnh từ máy tính** 
- ✅ **Lưu trữ trên cloud** với CDN tốc độ cao
- ✅ **Tự động cập nhật database**
- ✅ **Giao diện upload trực tiếp từ web**
- ✅ **Hỗ trợ nhiều định dạng**: JPG, PNG, WebP, GIF

## 📁 Cấu Trúc File

```
binhtoi/
├── images/                    # Thư mục chứa hình ảnh local
│   ├── README.md             # Hướng dẫn đặt tên file
│   ├── 25631630.png          # Hình ảnh sản phẩm (tên = SKU)
│   └── 25631647.jpg          # ...
├── upload_images.py          # Script upload hàng loạt
├── create_sample_images.py   # Tạo hình ảnh mẫu
└── index.html               # Giao diện web với tính năng upload
```

## 🚀 Cách Sử Dụng

### Phương Án 1: Upload Từ Web (Khuyến Nghị)

1. **Mở ứng dụng web**: `http://localhost:8001`
2. **Click nút "Upload"** ở góc trên bên phải
3. **Chọn sản phẩm** từ dropdown
4. **Chọn hình ảnh** từ máy tính
5. **Xem trước** và click "Upload"

### Phương Án 2: Upload Hàng Loạt

1. **Đặt hình ảnh vào thư mục `images/`**:
   ```
   images/25631630.jpg    # SKU: 25631630
   images/25631647.png    # SKU: 25631647
   images/25631654.webp   # SKU: 25631654
   ```

2. **Chạy script upload**:
   ```bash
   python3 upload_images.py
   ```

3. **Kết quả**:
   ```
   📸 Tìm thấy 3 file hình ảnh
   📦 Có 32 sản phẩm trong database
   
   ✅ Thành công: 25631630
   ✅ Thành công: 25631647
   ✅ Thành công: 25631654
   
   📊 Kết quả: 3/3 thành công
   ```

### Phương Án 3: Tạo Hình Ảnh Mẫu

Nếu chưa có hình ảnh thật, có thể tạo hình ảnh mẫu:

```bash
python3 create_sample_images.py
```

## 📋 Quy Tắc Đặt Tên

- **Tên file = SKU sản phẩm**
- **Định dạng hỗ trợ**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`
- **Ví dụ**: 
  - SKU `25631630` → `25631630.jpg`
  - SKU `JA657` → `JA657.png`

## 🔧 Cấu Hình Supabase Storage

### Bucket Information
- **Bucket Name**: `product-images`
- **Public Access**: ✅ Enabled
- **File Size Limit**: 50MB
- **Allowed Types**: image/jpeg, image/png, image/webp, image/gif

### URL Format
```
https://zgrfqkytbmahxcbgpkxx.supabase.co/storage/v1/object/public/product-images/{sku}.{ext}
```

## 🛠️ Troubleshooting

### Lỗi Upload
```bash
❌ Lỗi upload: Header value must be str or bytes
```
**Giải pháp**: Cập nhật Supabase client hoặc kiểm tra định dạng file

### Lỗi Kết Nối
```bash
❌ Lỗi kết nối Supabase: Vui lòng cập nhật SUPABASE_URL và SUPABASE_KEY
```
**Giải pháp**: Kiểm tra file `.env` và `supabase_client.js`

### File Không Hiển Thị
1. **Kiểm tra URL**: Mở trực tiếp URL hình ảnh
2. **Clear cache**: Refresh trang web (Ctrl+F5)
3. **Kiểm tra database**: Xem trường `image` trong bảng `products`

## 📊 Monitoring

### Kiểm Tra Storage
```sql
-- Xem danh sách file đã upload
SELECT name, size, created_at 
FROM storage.objects 
WHERE bucket_id = 'product-images'
ORDER BY created_at DESC;
```

### Kiểm Tra Database
```sql
-- Xem sản phẩm có hình ảnh
SELECT sku, name, image 
FROM products 
WHERE image LIKE '%supabase%'
ORDER BY sku;
```

## 🎨 Tùy Chỉnh

### Thay Đổi Kích Thước Hiển Thị
Sửa CSS trong `index.html`:
```css
.product-card img {
    height: 160px; /* Thay đổi chiều cao */
}
```

### Thêm Watermark
Sửa `create_sample_images.py` để thêm logo/watermark

### Tối Ưu Hình Ảnh
Thêm compression trong script upload:
```python
from PIL import Image

# Resize và compress
img = Image.open(file_path)
img = img.resize((400, 400), Image.Resampling.LANCZOS)
img.save(output_path, optimize=True, quality=85)
```

## 🔐 Bảo Mật

- ✅ **Public bucket** cho hình ảnh sản phẩm (OK)
- ✅ **File size limit** 50MB
- ✅ **MIME type validation**
- ⚠️ **Chỉ admin** nên có quyền upload

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra console log trong browser (F12)
2. Xem log server: `python3 -m http.server 8001`
3. Test kết nối Supabase: `python3 supabase_sync.py`

---

🎉 **Chúc mừng!** Hệ thống quản lý hình ảnh đã sẵn sàng sử dụng!
