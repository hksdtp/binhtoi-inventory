#!/usr/bin/env python3
"""
Test script để kiểm tra đồng bộ hoàn chỉnh với Supabase
"""
import json
from supabase_config import get_supabase_client

def test_database_connection():
    """Test kết nối database"""
    print("🔗 Testing database connection...")
    try:
        supabase = get_supabase_client()
        response = supabase.table('products').select('count').execute()
        print(f"✅ Database connected - Found {len(response.data)} products")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_storage_connection():
    """Test kết nối storage"""
    print("🗄️ Testing storage connection...")
    try:
        supabase = get_supabase_client()
        response = supabase.storage.list_buckets()
        buckets = [bucket.name for bucket in response]
        print(f"✅ Storage connected - Found buckets: {buckets}")
        return 'product-images' in buckets
    except Exception as e:
        print(f"❌ Storage connection failed: {e}")
        return False

def test_products_with_images():
    """Test sản phẩm có hình ảnh"""
    print("🖼️ Testing products with images...")
    try:
        supabase = get_supabase_client()
        response = supabase.table('products').select('sku, name, image').execute()
        
        products_with_supabase_images = [
            p for p in response.data 
            if p.get('image') and 'supabase' in p['image']
        ]
        
        print(f"✅ Found {len(products_with_supabase_images)} products with Supabase images:")
        for product in products_with_supabase_images[:5]:  # Show first 5
            print(f"   📦 {product['sku']}: {product['name']}")
            
        return len(products_with_supabase_images) > 0
    except Exception as e:
        print(f"❌ Failed to check products: {e}")
        return False

def test_image_urls():
    """Test URL hình ảnh có accessible không"""
    print("🌐 Testing image URL accessibility...")
    try:
        import requests
        supabase = get_supabase_client()
        response = supabase.table('products').select('sku, image').limit(3).execute()
        
        accessible_count = 0
        for product in response.data:
            if product.get('image') and 'supabase' in product['image']:
                try:
                    img_response = requests.head(product['image'], timeout=5)
                    if img_response.status_code == 200:
                        accessible_count += 1
                        print(f"   ✅ {product['sku']}: Image accessible")
                    else:
                        print(f"   ❌ {product['sku']}: Image not accessible ({img_response.status_code})")
                except Exception as e:
                    print(f"   ❌ {product['sku']}: Error checking image - {e}")
        
        print(f"✅ {accessible_count} images are accessible")
        return accessible_count > 0
    except ImportError:
        print("⚠️ requests module not available, skipping URL test")
        return True
    except Exception as e:
        print(f"❌ Failed to test image URLs: {e}")
        return False

def test_web_app_data_source():
    """Test xem web app đang load từ đâu"""
    print("📱 Testing web app data source...")
    try:
        # Kiểm tra file local
        with open('products_data.json', 'r', encoding='utf-8') as f:
            local_data = json.load(f)
        
        # Kiểm tra Supabase
        supabase = get_supabase_client()
        response = supabase.table('products').select('*').execute()
        supabase_data = response.data
        
        print(f"📄 Local JSON: {len(local_data)} products")
        print(f"☁️ Supabase: {len(supabase_data)} products")
        
        # So sánh một vài sản phẩm
        if local_data and supabase_data:
            local_first = local_data[0]
            supabase_first = next((p for p in supabase_data if p['sku'] == local_first['sku']), None)
            
            if supabase_first:
                print(f"🔍 Comparing first product ({local_first['sku']}):")
                print(f"   Local image: {local_first.get('image', 'N/A')[:50]}...")
                print(f"   Supabase image: {supabase_first.get('image', 'N/A')[:50]}...")
                
                if 'supabase' in supabase_first.get('image', ''):
                    print("   ✅ Supabase has real image URLs")
                else:
                    print("   ⚠️ Supabase still has placeholder images")
        
        return True
    except Exception as e:
        print(f"❌ Failed to compare data sources: {e}")
        return False

def main():
    print("🧪 SUPABASE SYNC TEST")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Storage Connection", test_storage_connection),
        ("Products with Images", test_products_with_images),
        ("Image URL Accessibility", test_image_urls),
        ("Web App Data Source", test_web_app_data_source),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Supabase sync is working perfectly!")
    elif passed >= total * 0.8:
        print("✅ Most tests passed. Minor issues may exist.")
    else:
        print("⚠️ Several tests failed. Please check configuration.")
    
    print("\n💡 RECOMMENDATIONS:")
    if passed < total:
        print("   1. Check .env file configuration")
        print("   2. Verify Supabase project settings")
        print("   3. Run: python3 supabase_sync.py")
        print("   4. Run: python3 upload_images.py")
    else:
        print("   1. Your Supabase integration is working!")
        print("   2. Web app should load data from Supabase")
        print("   3. Image upload should work from web interface")

if __name__ == "__main__":
    main()
