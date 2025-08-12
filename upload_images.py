#!/usr/bin/env python3
"""
Script upload hình ảnh sản phẩm lên Supabase Storage
"""
import os
import json
import mimetypes
from pathlib import Path
from supabase_config import get_supabase_client

def create_images_folder():
    """Tạo thư mục images nếu chưa có"""
    images_dir = Path("images")
    if not images_dir.exists():
        images_dir.mkdir()
        print(f"📁 Đã tạo thư mục: {images_dir}")
        
        # Tạo file README hướng dẫn
        readme_content = """# Thư mục hình ảnh sản phẩm

Đặt hình ảnh sản phẩm vào thư mục này với tên file theo format:
- {sku}.jpg
- {sku}.png  
- {sku}.webp

Ví dụ:
- 25631630.jpg (cho sản phẩm có SKU: 25631630)
- 25631647.png (cho sản phẩm có SKU: 25631647)

Sau đó chạy: python3 upload_images.py
"""
        with open(images_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        return False
    return True

def get_image_files():
    """Lấy danh sách file hình ảnh trong thư mục images"""
    images_dir = Path("images")
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    
    image_files = []
    for file_path in images_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return image_files

def upload_image_to_supabase(file_path, sku):
    """Upload một hình ảnh lên Supabase Storage"""
    try:
        supabase = get_supabase_client()
        
        # Đọc file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Xác định MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = 'image/jpeg'
        
        # Tên file trên storage
        file_name = f"{sku}{file_path.suffix.lower()}"
        
        # Thử xóa file cũ trước (nếu có)
        try:
            supabase.storage.from_("product-images").remove([file_name])
        except:
            pass  # Ignore nếu file không tồn tại

        # Upload file
        response = supabase.storage.from_("product-images").upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": mime_type}
        )

        # Kiểm tra response
        if hasattr(response, 'status_code'):
            success = response.status_code == 200
        elif hasattr(response, 'statusCode'):
            success = response.statusCode == 200 or response.statusCode == 409  # 409 = file exists, OK
        else:
            # Với Supabase Python client mới, kiểm tra theo cách khác
            success = not hasattr(response, 'error') or response.error is None

        if success:
            # Lấy public URL
            public_url = supabase.storage.from_("product-images").get_public_url(file_name)
            return public_url
        else:
            print(f"❌ Lỗi upload {file_name}: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Lỗi upload {file_path.name}: {e}")
        return None

def update_product_image_url(sku, image_url):
    """Cập nhật URL hình ảnh trong database"""
    try:
        supabase = get_supabase_client()
        
        response = supabase.table('products').update({
            'image': image_url
        }).eq('sku', sku).execute()
        
        if response.data:
            return True
        else:
            print(f"❌ Không tìm thấy sản phẩm với SKU: {sku}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi cập nhật database cho SKU {sku}: {e}")
        return False

def load_products_data():
    """Đọc dữ liệu sản phẩm để lấy danh sách SKU"""
    try:
        with open('products_data.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        return {product['sku']: product['name'] for product in products if 'sku' in product}
    except Exception as e:
        print(f"❌ Lỗi đọc products_data.json: {e}")
        return {}

def main():
    print("🖼️  Script Upload Hình Ảnh Sản Phẩm")
    print("=" * 50)
    
    # Kiểm tra thư mục images
    if not create_images_folder():
        print("📝 Vui lòng đặt hình ảnh vào thư mục 'images' và chạy lại script")
        return
    
    # Lấy danh sách file hình ảnh
    image_files = get_image_files()
    if not image_files:
        print("📁 Không tìm thấy file hình ảnh nào trong thư mục 'images'")
        print("💡 Đặt file hình ảnh với tên theo SKU (ví dụ: 25631630.jpg)")
        return
    
    # Lấy danh sách sản phẩm
    products = load_products_data()
    if not products:
        print("❌ Không thể đọc dữ liệu sản phẩm")
        return
    
    print(f"📸 Tìm thấy {len(image_files)} file hình ảnh")
    print(f"📦 Có {len(products)} sản phẩm trong database")
    print()
    
    success_count = 0
    error_count = 0
    
    for image_file in image_files:
        # Lấy SKU từ tên file (bỏ extension)
        sku = image_file.stem
        
        if sku not in products:
            print(f"⚠️  Không tìm thấy sản phẩm với SKU: {sku}")
            error_count += 1
            continue
        
        print(f"📤 Đang upload: {image_file.name} cho sản phẩm '{products[sku]}'")
        
        # Upload hình ảnh
        image_url = upload_image_to_supabase(image_file, sku)
        if not image_url:
            error_count += 1
            continue
        
        # Cập nhật database
        if update_product_image_url(sku, image_url):
            print(f"✅ Thành công: {sku}")
            success_count += 1
        else:
            error_count += 1
    
    print()
    print("📊 Kết quả upload:")
    print(f"   ✅ Thành công: {success_count}")
    print(f"   ❌ Lỗi: {error_count}")
    print(f"   📦 Tổng: {success_count + error_count}")

if __name__ == "__main__":
    main()
