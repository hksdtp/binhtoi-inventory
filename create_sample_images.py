#!/usr/bin/env python3
"""
Tạo hình ảnh mẫu cho sản phẩm
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random

def create_product_image(sku, product_name, category, size=(400, 400)):
    """Tạo hình ảnh sản phẩm với thông tin cơ bản"""
    
    # Màu sắc theo category
    category_colors = {
        "Bình để nến": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"],
        "Cốc sứ": ["#FECA57", "#FF9FF3", "#54A0FF", "#5F27CD"],
        "default": ["#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE"]
    }
    
    colors = category_colors.get(category, category_colors["default"])
    bg_color = random.choice(colors)
    
    # Tạo image
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Vẽ hình dạng sản phẩm
    if "Bình" in product_name:
        # Vẽ hình bình
        draw.ellipse([size[0]//3, size[1]//4, 2*size[0]//3, 3*size[1]//4], 
                    fill='white', outline='#333', width=3)
        draw.rectangle([size[0]//3 + 20, size[1]//4 - 20, 2*size[0]//3 - 20, size[1]//4 + 10], 
                      fill='#FFD700', outline='#333', width=2)
    elif "Cốc" in product_name:
        # Vẽ hình cốc
        draw.rectangle([size[0]//3, size[1]//3, 2*size[0]//3, 3*size[1]//4], 
                      fill='white', outline='#333', width=3)
        draw.arc([size[0]//3 + 10, size[1]//3 - 10, 2*size[0]//3 - 10, size[1]//3 + 20], 
                 0, 180, fill='#333', width=3)
    
    # Thêm text
    try:
        # Thử sử dụng font hệ thống
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # SKU ở góc trên
    draw.text((10, 10), f"SKU: {sku}", fill='#333', font=font_small)
    
    # Tên sản phẩm ở dưới (rút gọn)
    short_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    text_bbox = draw.textbbox((0, 0), short_name, font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (size[0] - text_width) // 2
    draw.text((text_x, size[1] - 60), short_name, fill='#333', font=font_large)
    
    return img

def main():
    print("🎨 Tạo hình ảnh mẫu cho sản phẩm")
    print("=" * 40)
    
    # Đọc dữ liệu sản phẩm
    try:
        with open('products_data.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"❌ Lỗi đọc products_data.json: {e}")
        return
    
    images_dir = Path("images")
    if not images_dir.exists():
        images_dir.mkdir()
    
    created_count = 0
    
    # Tạo hình ảnh cho 5 sản phẩm đầu tiên làm mẫu
    for i, product in enumerate(products[:5]):
        if 'sku' not in product:
            continue
            
        sku = product['sku']
        name = product['name']
        category = product.get('category', 'default')
        
        # Tạo hình ảnh
        img = create_product_image(sku, name, category)
        
        # Lưu file
        image_path = images_dir / f"{sku}.png"
        img.save(image_path)
        
        print(f"✅ Đã tạo: {image_path.name} - {name}")
        created_count += 1
    
    print(f"\n📊 Đã tạo {created_count} hình ảnh mẫu")
    print("💡 Bạn có thể thay thế bằng hình ảnh thật và chạy: python3 upload_images.py")

if __name__ == "__main__":
    main()
