#!/usr/bin/env python3
"""
Flask server with image upload API for inventory management
"""

import os
import json
import mimetypes
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import Supabase config
try:
    from supabase_config import get_supabase_client
    SUPABASE_AVAILABLE = True
except:
    SUPABASE_AVAILABLE = False
    print("⚠️  Supabase không khả dụng - sẽ lưu ảnh local")

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_products():
    """Load products data"""
    try:
        with open('products_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_products(products):
    """Save products data"""
    try:
        with open('products_data.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def upload_to_supabase(file_path, sku):
    """Upload image to Supabase Storage"""
    if not SUPABASE_AVAILABLE:
        return None
    
    try:
        supabase = get_supabase_client()
        
        # Read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Get MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if not mime_type:
            mime_type = 'image/jpeg'
        
        # File name on storage
        file_name = f"{sku}{Path(file_path).suffix.lower()}"
        
        # Try to remove old file first
        try:
            supabase.storage.from_("product-images").remove([file_name])
        except:
            pass
        
        # Upload file
        response = supabase.storage.from_("product-images").upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": mime_type}
        )
        
        # Check response
        success = False
        if hasattr(response, 'status_code'):
            success = response.status_code == 200
        elif hasattr(response, 'statusCode'):
            success = response.statusCode in [200, 409]  # 409 = file exists, OK
        else:
            success = not hasattr(response, 'error') or response.error is None
        
        if success:
            # Get public URL
            public_url = supabase.storage.from_("product-images").get_public_url(file_name)
            return public_url
        else:
            print(f"❌ Supabase upload error: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Supabase upload exception: {e}")
        return None

def update_product_image_supabase(sku, image_url):
    """Update product image URL in Supabase database"""
    if not SUPABASE_AVAILABLE:
        return False
    
    try:
        supabase = get_supabase_client()
        response = supabase.table('products').update({
            'image': image_url
        }).eq('sku', sku).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"❌ Supabase DB update error: {e}")
        return False

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/products')
def get_products():
    products = load_products()
    return jsonify(products)

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Upload single or multiple images for a product"""
    
    # Check if files are in request
    if 'files' not in request.files and 'file' not in request.files:
        return jsonify({'error': 'Không có file được chọn'}), 400
    
    # Handle both single and multiple file uploads
    files = request.files.getlist('files') if 'files' in request.files else [request.files['file']]
    sku = request.form.get('sku', '').strip()
    
    if not files or all(f.filename == '' for f in files):
        return jsonify({'error': 'Không có file được chọn'}), 400
    
    if not sku:
        return jsonify({'error': 'SKU không được để trống'}), 400
    
    # Check file types
    for file in files:
        if file.filename and not allowed_file(file.filename):
            return jsonify({'error': f'File {file.filename} không được hỗ trợ. Chỉ chấp nhận: png, jpg, jpeg, gif, webp'}), 400
    
    try:
        # Load products to check if SKU exists
        products = load_products()
        product = next((p for p in products if p.get('sku') == sku), None)
        
        if not product:
            return jsonify({'error': f'Không tìm thấy sản phẩm với SKU: {sku}'}), 404
        
        uploaded_images = []
        local_images = []
        
        for index, file in enumerate(files):
            if file.filename == '':
                continue
                
            # Generate filename with index for multiple images
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            if len(files) > 1:
                filename = f"{sku}_{index + 1}.{file_extension}"
            else:
                filename = f"{sku}.{file_extension}"
            
            # Save file locally first
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_path)
            
            # Try to upload to Supabase
            image_url = upload_to_supabase(local_path, f"{sku}_{index + 1}" if len(files) > 1 else sku)
            
            if image_url:
                uploaded_images.append(image_url)
            else:
                # Fallback to local file
                local_url = f"/images/{filename}"
                local_images.append(local_url)
        
        # Update product with images
        all_images = uploaded_images + local_images
        
        if len(all_images) == 1:
            # Single image - maintain backward compatibility
            product['image'] = all_images[0]
            if 'images' in product:
                del product['images']
        else:
            # Multiple images
            product['images'] = all_images
            product['image'] = all_images[0]  # First image as primary
        
        # Update Supabase database
        supabase_updated = False
        if SUPABASE_AVAILABLE:
            try:
                supabase = get_supabase_client()
                update_data = {
                    'image': product['image']
                }
                if 'images' in product:
                    update_data['images'] = product['images']
                
                response = supabase.table('products').update(update_data).eq('sku', sku).execute()
                supabase_updated = bool(response.data)
            except Exception as e:
                print(f"❌ Supabase DB update error: {e}")
        
        # Save local JSON
        save_products(products)
        
        return jsonify({
            'message': f'Upload thành công {len(all_images)} ảnh!',
            'images': all_images,
            'primary_image': all_images[0],
            'sku': sku,
            'product_name': product.get('name'),
            'supabase_synced': supabase_updated
        })
    
    except Exception as e:
        return jsonify({'error': f'Lỗi upload: {str(e)}'}), 500

@app.route('/api/products/<sku>/image', methods=['DELETE'])
def delete_product_image(sku):
    """Delete product image"""
    try:
        products = load_products()
        product = next((p for p in products if p.get('sku') == sku), None)
        
        if not product:
            return jsonify({'error': 'Không tìm thấy sản phẩm'}), 404
        
        # Clear image URL
        product['image'] = ''
        save_products(products)
        
        return jsonify({'message': 'Đã xóa ảnh sản phẩm'})
    
    except Exception as e:
        return jsonify({'error': f'Lỗi xóa ảnh: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Flask server starting...")
    print(f"📱 Web app: http://localhost:8000")
    print(f"🖼️  Upload API: http://localhost:8000/api/upload")
    print(f"📊 Supabase: {'✅ Available' if SUPABASE_AVAILABLE else '❌ Not configured'}")
    
    app.run(host='0.0.0.0', port=8000, debug=True)