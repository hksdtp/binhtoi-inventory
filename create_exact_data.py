#!/usr/bin/env python3
"""
Tạo dữ liệu chính xác từ bảng được cung cấp
"""

import json

def generate_product_image(category):
    """Tạo SVG image dựa trên category"""
    if "nến" in category.lower():
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23F5F8FA'/%3E%3Crect x='85' y='60' width='30' height='80' fill='%23F4C2A1' stroke='%234A90A4' stroke-width='2'/%3E%3Cellipse cx='100' cy='60' rx='15' ry='8' fill='%23FFD700'/%3E%3Cpath d='M100 52 Q105 45 100 40' stroke='%23FF6B35' stroke-width='2' fill='none'/%3E%3C/svg%3E"
    elif "đốt" in category.lower() or "tinh dầu" in category.lower():
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23F5F8FA'/%3E%3Cellipse cx='100' cy='160' rx='25' ry='8' fill='%23E0E0E0'/%3E%3Cpath d='M75 160 Q75 90 100 80 Q125 90 125 160' fill='%23F0F0F0' stroke='%234A90A4' stroke-width='2'/%3E%3Ccircle cx='100' cy='85' r='3' fill='%23FF6B35'/%3E%3C/svg%3E"
    elif "cốc" in category.lower():
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23F5F8FA'/%3E%3Cpath d='M70 80 L70 140 Q70 150 80 150 L120 150 Q130 150 130 140 L130 80 Z' fill='%23F0F0F0' stroke='%234A90A4' stroke-width='2'/%3E%3Cpath d='M130 100 Q140 100 140 110 Q140 120 130 120' stroke='%234A90A4' stroke-width='2' fill='none'/%3E%3C/svg%3E"
    else:
        return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23F5F8FA'/%3E%3Crect x='40' y='40' width='120' height='120' fill='%23E0E0E0' stroke='%234A90A4' stroke-width='2'/%3E%3Ctext x='100' y='105' text-anchor='middle' fill='%23666' font-size='12'%3ESản phẩm%3C/text%3E%3C/svg%3E"

# Dữ liệu chính xác từ bảng
raw_data = [
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

def get_category_from_name(name):
    """Xác định category dựa trên tên sản phẩm"""
    name_lower = name.lower()
    
    if "bình để nến" in name_lower or "bình decor" in name_lower:
        return "Bình để nến"
    elif "bình đốt tinh dầu" in name_lower or "bình décor miri" in name_lower:
        return "Bình xông đốt tinh dầu"
    elif "cốc" in name_lower:
        return "Cốc nến thơm"
    else:
        return "Khác"

# Tạo dữ liệu products
products = []
for i, (sku, original_name, display_name, stock) in enumerate(raw_data, 1):
    category = get_category_from_name(display_name)
    image = generate_product_image(category)
    
    product = {
        'id': i,
        'name': display_name,
        'category': category,
        'stock': stock,
        'price': 0,  # Không có giá trong dữ liệu gốc
        'description': f'Mã: {sku}',
        'image': image,
        'sku': sku
    }
    
    products.append(product)

# Xuất ra file JSON
with open('products_data.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print(f'✅ Đã tạo {len(products)} sản phẩm chính xác từ bảng dữ liệu')

# Thống kê
total_stock = sum(p['stock'] for p in products)
categories = {}
for p in products:
    cat = p['category']
    if cat not in categories:
        categories[cat] = {'count': 0, 'stock': 0}
    categories[cat]['count'] += 1
    categories[cat]['stock'] += p['stock']

print(f'\n📊 Thống kê:')
print(f'- Tổng số sản phẩm: {len(products)}')
print(f'- Tổng tồn kho: {total_stock}')
print(f'- Theo danh mục:')
for cat, stats in sorted(categories.items(), key=lambda x: x[1]['stock'], reverse=True):
    print(f'  + {cat}: {stats["count"]} sản phẩm, {stats["stock"]} tồn')

# Kiểm tra tổng
expected_total = 2602
if total_stock == expected_total:
    print(f'✅ Tổng tồn kho khớp: {total_stock}')
else:
    print(f'❌ Tổng tồn kho không khớp: {total_stock} (mong đợi: {expected_total})')
