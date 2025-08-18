#!/usr/bin/env python3
"""
Script để tạo Open Graph image cho website
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_og_image():
    """Tạo Open Graph image 1200x630px"""
    
    # Kích thước chuẩn OG image
    width, height = 1200, 630
    
    # Tạo gradient background
    img = Image.new('RGB', (width, height), color='#667eea')
    draw = ImageDraw.Draw(img)
    
    # Tạo gradient từ xanh dương đến tím
    for y in range(height):
        # Tính toán màu gradient
        ratio = y / height
        r = int(102 + (118 - 102) * ratio)  # 667eea -> 764ba2
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Vẽ background overlay
    overlay_color = (255, 255, 255, 30)  # Trắng với alpha
    draw.rounded_rectangle(
        [150, 150, width-150, height-150], 
        radius=20, 
        fill=overlay_color
    )
    
    try:
        # Thử load font system
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Text content
    title = "Kho Bình Cốc Tồn"
    subtitle = "Quản lý tồn kho thông minh"
    description = "Bình để nến • Bình đốt tinh dầu • Cốc sứ deco"
    
    # Tính toán vị trí text (center)
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    title_y = 200
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 100
    
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (width - desc_width) // 2
    desc_y = subtitle_y + 80
    
    # Vẽ text với shadow
    shadow_offset = 3
    shadow_color = (0, 0, 0, 100)
    text_color = (255, 255, 255, 255)
    
    # Title shadow và text
    draw.text((title_x + shadow_offset, title_y + shadow_offset), title, 
              fill=shadow_color, font=title_font)
    draw.text((title_x, title_y), title, fill=text_color, font=title_font)
    
    # Subtitle
    draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), subtitle, 
              fill=shadow_color, font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle, fill=text_color, font=subtitle_font)
    
    # Description
    draw.text((desc_x + shadow_offset, desc_y + shadow_offset), description, 
              fill=shadow_color, font=desc_font)
    draw.text((desc_x, desc_y), description, fill=text_color, font=desc_font)
    
    # Vẽ icon/emoji (nếu có font hỗ trợ)
    icon = "🏺"
    icon_y = 120
    try:
        icon_bbox = draw.textbbox((0, 0), icon, font=title_font)
        icon_width = icon_bbox[2] - icon_bbox[0]
        icon_x = (width - icon_width) // 2
        draw.text((icon_x, icon_y), icon, fill=text_color, font=title_font)
    except:
        # Vẽ circle thay thế nếu không có emoji
        circle_x, circle_y = width // 2, icon_y + 40
        draw.ellipse([circle_x-30, circle_y-30, circle_x+30, circle_y+30], 
                    fill=(255, 255, 255, 150))
    
    # Vẽ decorative elements
    # Circle 1
    draw.ellipse([width-150, -50, width+50, 150], fill=(255, 255, 255, 20))
    # Circle 2
    draw.ellipse([-75, height-75, 75, height+75], fill=(255, 255, 255, 20))
    # Circle 3
    draw.ellipse([100, height//2-50, 200, height//2+50], fill=(255, 255, 255, 10))
    
    # Lưu file
    output_path = "images/og-image.jpg"
    os.makedirs("images", exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    
    print(f"✅ Đã tạo Open Graph image: {output_path}")
    print(f"📐 Kích thước: {width}x{height}px")
    return output_path

if __name__ == "__main__":
    create_og_image()
