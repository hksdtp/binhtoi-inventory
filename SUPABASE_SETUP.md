# Hướng dẫn kết nối Supabase

## 1. Tạo dự án Supabase

1. Đăng ký tài khoản tại [supabase.com](https://supabase.com)
2. Tạo dự án mới
3. Lấy thông tin kết nối:
   - **Project URL**: `https://your-project-id.supabase.co`
   - **Anon key**: Từ Settings > API

## 2. Cài đặt dependencies

```bash
pip install supabase python-dotenv
```

## 3. Cấu hình kết nối

1. Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

2. Cập nhật thông tin trong `.env`:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
```

3. Cập nhật thông tin trong `supabase_client.js`:
```javascript
this.supabaseUrl = 'https://your-project-id.supabase.co';
this.supabaseKey = 'your-anon-key-here';
```

## 4. Tạo bảng trong Supabase

Chạy SQL sau trong Supabase Dashboard > SQL Editor:

```sql
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    stock INTEGER DEFAULT 0,
    price NUMERIC DEFAULT 0,
    description TEXT,
    image TEXT,
    sku TEXT UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

-- Tạo trigger để tự động cập nhật updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc'::text, NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_products_updated_at BEFORE UPDATE
    ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 5. Đồng bộ dữ liệu

```bash
python3 supabase_sync.py
```

Chọn option 1 để sync dữ liệu local lên Supabase.

## 6. Test kết nối

1. Khởi động web server:
```bash
python3 server.py
```

2. Mở http://localhost:8000
3. Kiểm tra console log để xem trạng thái kết nối
4. Thử nút "Sync" để test đồng bộ

## Tính năng

- ✅ **Offline-first**: App hoạt động ngay cả khi mất mạng
- ✅ **Auto-sync**: Tự động đồng bộ khi có kết nối
- ✅ **Cache**: Lưu cache local để truy cập nhanh
- ✅ **Real-time**: Cập nhật dữ liệu real-time với Supabase
- ✅ **Backup**: Dữ liệu được backup an toàn trên cloud

## Troubleshooting

### Lỗi kết nối
- Kiểm tra SUPABASE_URL và SUPABASE_KEY
- Kiểm tra kết nối internet
- Xem console log để debug

### Lỗi sync
- Kiểm tra bảng `products` đã được tạo chưa
- Kiểm tra quyền truy cập trong Supabase
- Xem chi tiết lỗi trong console