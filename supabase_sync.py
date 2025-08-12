#!/usr/bin/env python3
"""
Script đồng bộ dữ liệu với Supabase
"""
import json
import os
from datetime import datetime
from supabase_config import get_supabase_client

def load_local_data():
    """Đọc dữ liệu từ file JSON local"""
    try:
        with open('products_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Không tìm thấy file products_data.json")
        return []
    except json.JSONDecodeError:
        print("❌ Lỗi đọc file JSON")
        return []

def sync_to_supabase(products_data):
    """Đồng bộ dữ liệu lên Supabase"""
    try:
        supabase = get_supabase_client()
        
        # Xóa dữ liệu cũ (tùy chọn)
        # supabase.table('products').delete().execute()
        
        success_count = 0
        error_count = 0
        
        for product in products_data:
            try:
                # Chuẩn bị dữ liệu (loại bỏ id để Supabase tự tạo)
                product_data = {
                    'name': product.get('name', ''),
                    'category': product.get('category', ''),
                    'stock': product.get('stock', 0),
                    'price': product.get('price', 0),
                    'description': product.get('description', ''),
                    'image': product.get('image', ''),
                    'sku': product.get('sku', '')
                }
                
                # Upsert dữ liệu (insert hoặc update nếu sku đã tồn tại)
                result = supabase.table('products').upsert(
                    product_data, 
                    on_conflict='sku'
                ).execute()
                
                if result.data:
                    success_count += 1
                    print(f"✅ Sync thành công: {product.get('name', 'N/A')}")
                else:
                    error_count += 1
                    print(f"❌ Lỗi sync: {product.get('name', 'N/A')}")
                    
            except Exception as e:
                error_count += 1
                print(f"❌ Lỗi sync {product.get('name', 'N/A')}: {str(e)}")
        
        print(f"\n📊 Kết quả sync:")
        print(f"   ✅ Thành công: {success_count}")
        print(f"   ❌ Lỗi: {error_count}")
        print(f"   📦 Tổng: {len(products_data)}")
        
        return success_count, error_count
        
    except Exception as e:
        print(f"❌ Lỗi kết nối Supabase: {str(e)}")
        return 0, len(products_data)

def sync_from_supabase():
    """Lấy dữ liệu từ Supabase và lưu local"""
    try:
        supabase = get_supabase_client()
        
        # Lấy tất cả products
        result = supabase.table('products').select('*').execute()
        
        if result.data:
            # Lưu vào file JSON
            with open('products_data_supabase.json', 'w', encoding='utf-8') as f:
                json.dump(result.data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Đã tải {len(result.data)} sản phẩm từ Supabase")
            return result.data
        else:
            print("📭 Không có dữ liệu trong Supabase")
            return []
            
    except Exception as e:
        print(f"❌ Lỗi tải dữ liệu từ Supabase: {str(e)}")
        return []

def main():
    print("🔄 Bắt đầu đồng bộ dữ liệu với Supabase...")
    print("=" * 50)
    
    # Kiểm tra file .env
    if not os.path.exists('.env'):
        print("⚠️  Chưa có file .env. Tạo file .env từ .env.example và cập nhật thông tin Supabase")
        return
    
    # Menu chọn
    print("Chọn hành động:")
    print("1. Sync dữ liệu local lên Supabase")
    print("2. Tải dữ liệu từ Supabase về local")
    print("3. Cả hai (sync lên rồi tải về)")
    
    choice = input("Nhập lựa chọn (1-3): ").strip()
    
    if choice == "1":
        products = load_local_data()
        if products:
            sync_to_supabase(products)
    
    elif choice == "2":
        sync_from_supabase()
    
    elif choice == "3":
        products = load_local_data()
        if products:
            success, errors = sync_to_supabase(products)
            if success > 0:
                print("\n" + "=" * 50)
                sync_from_supabase()
    
    else:
        print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()