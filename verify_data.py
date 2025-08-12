#!/usr/bin/env python3
"""
Kiểm tra dữ liệu chính xác với bảng gốc
"""

import json

# Dữ liệu gốc từ bảng
original_data = [
    ["25631630", "Bình để nến Amiri, hồng bóng nhỏ", "Bình decor Amiri, hồng bóng nhỏ", 37],
    ["25631647", "Bình để nến Amiri, hồng mờ nhỏ", "Bình decor Amiri, hồng mờ nhỏ", 98],
    ["25631654", "Bình để nến Amiri, xanh biển bóng nhỏ", "Bình decor Amiri, xanh biển bóng nhỏ", 43],
    ["25631661", "Bình để nến Amiri, xanh mờ nhỏ", "Bình decor Amiri, xanh mờ nhỏ", 91],
    ["25631678", "Bình để nến Amiri, Xanh lá cây bóng", "Bình decor Amiri, Xanh lá cây bóng", 100],
    ["25631685", "Bình để nến Amiri, xám mờ nhỏ", "Bình decor Amiri, xám mờ nhỏ", 104],
    ["25631692", "Bình để nến Amiri, đen mờ nhỏ", "Bình decor Amiri, đen mờ nhỏ", 64],
    ["25631708", "Bình để nến Amiri, trắng bóng nhỏ", "Bình decor Amiri, trắng bóng nhỏ", 95],
    ["25631715", "Bình để nến Amiri, trắng mờ nhỏ", "Bình decor Amiri, trắng mờ nhỏ", 94],
    ["25631722", "Bình đốt tinh dầu Amiri, Hồng bóng, S", "Bình décor Miri, Hồng bóng, S", 38],
    ["25631739", "Bình đốt tinh dầu Amiri, Hồng mờ, S", "Bình décor Miri, Hồng mờ, S", 39],
    ["25631746", "Bình đốt tinh dầu Amiri, Xanh bóng, S", "Bình décor Miri, Xanh bóng, S", 47],
    ["25631753", "Bình đốt tinh dầu Amiri, Xanh mờ, S", "Bình décor Miri, Xanh mờ, S", 66],
    ["25631760", "Bình đốt tinh dầu Amiri, Xanh lá bóng, S", "Bình décor Miri, Xanh lá bóng, S", 84],
    ["25631777", "Bình đốt tinh dầu Amiri, Xám mờ, S", "Bình décor Miri, Xám mờ, S", 85],
    ["25631784", "Bình đốt tinh dầu Amiri, Đen mờ, S", "Bình décor Miri, Đen mờ, S", 75],
    ["25631791", "Bình đốt tinh dầu Amiri, Trắng bóng, S", "Bình décor Miri, Trắng bóng, S", 83],
    ["25631807", "Bình đốt tinh dầu Amiri, Trắng mờ, S", "Bình décor Miri, Trắng mờ, S", 90],
    ["25631814", "Bình đốt tinh dầu Amiri, Hồng bóng, M", "Bình décor Miri, Hồng bóng, M", 74],
    ["25631821", "Bình đốt tinh dầu Amiri, Hồng mờ, M", "Bình décor Miri, Hồng mờ, M", 98],
    ["25631838", "Bình đốt tinh dầu Amiri, Xanh bóng, M", "Bình décor Miri, Xanh bóng, M", 99],
    ["25631845", "Bình đốt tinh dầu Amiri, Xanh mờ, M", "Bình décor Miri, Xanh mờ, M", 97],
    ["25631852", "Bình đốt tinh dầu Amiri, Xanh lá bóng, M", "Bình décor Miri, Xanh lá bóng, M", 90],
    ["25631869", "Bình đốt tinh dầu Amiri, Xám mờ, M", "Bình décor Miri, Xám mờ, M", 107],
    ["25631876", "Bình đốt tinh dầu Amiri, Đen mờ, M", "Bình décor Miri, Đen mờ, M", 80],
    ["25631883", "Bình đốt tinh dầu Amiri, Trắng bóng, M", "Bình décor Miri, Trắng bóng, M", 90],
    ["25631890", "Bình đốt tinh dầu Amiri, Trắng mờ, M", "Bình décor Miri, Trắng mờ, M", 83],
    ["8935261208563", "Cốc sứ Deco JA657", "Cốc sứ Deco JA657", 81],
    ["8935261208570", "Cốc sứ Deco JA655", "Cốc sứ Deco JA655", 81],
    ["8935261208587", "Cốc sứ Deco JA656", "Cốc sứ Deco JA656", 78],
    ["8935261208594", "Cốc sứ Deco JA654", "Cốc sứ Deco JA654", 81],
    ["8935261208600", "Cốc sứ Deco JA028", "Cốc sứ Deco JA028", 130]
]

# Đọc dữ liệu từ JSON
with open('products_data.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print("🔍 KIỂM TRA DỮ LIỆU CHÍNH XÁC")
print("=" * 50)

errors = []
total_stock_original = sum(row[3] for row in original_data)
total_stock_json = sum(p['stock'] for p in products)

print(f"📊 Tổng số sản phẩm:")
print(f"   Gốc: {len(original_data)}")
print(f"   JSON: {len(products)}")
print(f"   Khớp: {'✅' if len(original_data) == len(products) else '❌'}")
print()

print(f"📊 Tổng tồn kho:")
print(f"   Gốc: {total_stock_original}")
print(f"   JSON: {total_stock_json}")
print(f"   Khớp: {'✅' if total_stock_original == total_stock_json else '❌'}")
print()

print("🔍 Kiểm tra từng sản phẩm:")
print("-" * 50)

for i, (sku, original_name, display_name, stock) in enumerate(original_data):
    # Tìm sản phẩm trong JSON
    product = next((p for p in products if p['sku'] == sku), None)
    
    if not product:
        errors.append(f"❌ Không tìm thấy SKU {sku}")
        continue
    
    # Kiểm tra các trường
    name_ok = product['name'] == display_name
    stock_ok = product['stock'] == stock
    price_ok = product['price'] == 0
    
    if name_ok and stock_ok and price_ok:
        print(f"✅ {sku}: {display_name} (Tồn: {stock})")
    else:
        print(f"❌ {sku}:")
        if not name_ok:
            print(f"   Tên sai: '{product['name']}' != '{display_name}'")
        if not stock_ok:
            print(f"   Tồn sai: {product['stock']} != {stock}")
        if not price_ok:
            print(f"   Giá sai: {product['price']} != 0")
        errors.append(f"SKU {sku} có lỗi")

print()
print("=" * 50)
if errors:
    print(f"❌ Có {len(errors)} lỗi:")
    for error in errors:
        print(f"   {error}")
else:
    print("✅ TẤT CẢ DỮ LIỆU CHÍNH XÁC 100%!")
    print("✅ Sẵn sàng sử dụng app!")

print()
print("📱 App: http://localhost:8000/index.html")
