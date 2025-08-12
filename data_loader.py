#!/usr/bin/env python3
"""
Script để đọc dữ liệu từ file Excel "Ton kho binh.xlsx" 
và chuyển đổi thành format JSON cho app
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import json
from collections import defaultdict

def col_to_index(col):
    """Chuyển đổi tên cột (A, B, C...) thành index số"""
    col = re.sub(r'[^A-Z]', '', col.upper())
    n = 0
    for ch in col:
        n = n*26 + (ord(ch)-64)
    return n-1 if n>0 else 0

def to_float(v):
    """Chuyển đổi giá trị thành float"""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        txt = v.replace('.', '').replace(',', '.')
        try:
            return float(txt)
        except:
            return None
    return None

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

def get_category_from_name(name):
    """Xác định category dựa trên tên sản phẩm"""
    name_lower = name.lower() if name else ""

    if "bình để nến" in name_lower or "bình decor" in name_lower:
        return "Bình để nến"
    elif "bình đốt tinh dầu" in name_lower or "bình décor miri" in name_lower:
        return "Bình xông đốt tinh dầu"
    elif "cốc" in name_lower:
        return "Cốc nến thơm"
    else:
        return "Khác"

def read_excel_data(file_path):
    """Đọc dữ liệu từ file Excel"""
    try:
        zf = zipfile.ZipFile(file_path)
    except Exception as e:
        print(f'[ERROR] Không mở được file Excel: {e}')
        return []

    # Đọc workbook và relationships
    workbook_xml = ET.fromstring(zf.read('xl/workbook.xml'))
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    rels_root = ET.fromstring(zf.read('xl/_rels/workbook.xml.rels'))
    rid_to_target = {
        rel.attrib.get('Id'): rel.attrib.get('Target') 
        for rel in rels_root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
    }

    # Lấy sheet đầu tiên
    sheets = []
    for sh in workbook_xml.findall('ns:sheets/ns:sheet', ns):
        name = sh.attrib.get('name')
        rid = sh.attrib.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
        target = rid_to_target.get(rid)
        if target and not target.startswith('/'):
            target = 'xl/' + target
        sheets.append((name, target))

    if not sheets:
        print('[ERROR] Không tìm thấy sheet nào')
        return []

    sheet_name, sheet_path = sheets[0]
    root = ET.fromstring(zf.read(sheet_path))

    # Load shared strings
    shared_strings = []
    try:
        sst_root = ET.fromstring(zf.read('xl/sharedStrings.xml'))
        for si in sst_root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
            texts = []
            for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                texts.append(t.text or '')
            shared_strings.append(''.join(texts))
    except KeyError:
        pass

    # Đọc dữ liệu từ các dòng
    rows_data = []
    for row in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
        row_dict = {}
        for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
            r = c.attrib.get('r', '')
            t = c.attrib.get('t')
            v_el = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            is_el = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is')
            val = None
            
            if t == 's':
                if v_el is not None and v_el.text is not None:
                    idx = int(v_el.text)
                    val = shared_strings[idx] if 0 <= idx < len(shared_strings) else None
            elif t == 'inlineStr' and is_el is not None:
                tnode = is_el.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                val = tnode.text if tnode is not None else None
            else:
                if v_el is not None and v_el.text is not None:
                    txt = v_el.text
                    try:
                        if '.' in txt or 'E' in txt or 'e' in txt:
                            val = float(txt)
                        else:
                            val = int(txt)
                    except Exception:
                        val = txt
            
            if r:
                col_letters = re.sub(r'[^A-Z]', '', r)
                row_dict[col_letters] = val
        rows_data.append(row_dict)

    # Tìm dòng header
    header_keywords = ['mã hàng', 'tên hàng', 'tồn', 'nhóm hàng']
    header_idx = 0
    best_score = -1
    for idx, rd in enumerate(rows_data):
        values = [str(v).strip().lower() for v in rd.values() if v is not None and str(v).strip()!='']
        score = sum(1 for kw in header_keywords if any(kw in v for v in values))
        if score > best_score:
            best_score = score
            header_idx = idx

    header_row = rows_data[header_idx]
    cols = sorted(header_row.keys(), key=col_to_index)
    headers = [str(header_row.get(c, '')).strip() for c in cols]

    # Xác định các trường
    h_lower = [h.lower() for h in headers]
    
    def find_field(kw_list):
        for i, h in enumerate(h_lower):
            if any(kw in h for kw in kw_list):
                return headers[i]
        return None

    sku_field = find_field(['mã hàng'])
    name_field = find_field(['tên hàng'])
    rename_field = find_field(['đổi tên'])
    qty_field = find_field(['tồn'])
    cat_field = find_field(['nhóm hàng'])

    # Xử lý dữ liệu
    products = []
    product_id = 1
    
    for rd in rows_data[header_idx+1:]:
        rec = {headers[i]: rd.get(cols[i]) for i in range(len(cols))}
        
        # Bỏ qua dòng rỗng
        if all((v is None or str(v).strip()=='') for v in rec.values()):
            continue
            
        # Bỏ qua dòng tổng hợp (không có SKU hoặc tên)
        sku = str(rec.get(sku_field) or '').strip()
        name = str(rec.get(name_field) or '').strip()
        if not sku or not name:
            continue
            
        qty = to_float(rec.get(qty_field)) if qty_field else 0
        if qty is None:
            qty = 0

        # Sử dụng tên đổi nếu có, không thì dùng tên gốc
        display_name = str(rec.get(rename_field) or '').strip()
        if not display_name:
            display_name = name

        # Xác định category từ tên sản phẩm
        category = get_category_from_name(display_name)
        image = generate_product_image(category)

        product = {
            'id': product_id,
            'name': display_name,
            'category': category,
            'stock': int(qty),
            'price': 0,  # Không có giá trong dữ liệu gốc
            'description': f'Mã: {sku}',
            'image': image,
            'sku': sku
        }
        
        products.append(product)
        product_id += 1

    return products

if __name__ == '__main__':
    products = read_excel_data('Ton kho binh.xlsx')
    
    # Xuất ra file JSON
    with open('products_data.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f'Đã xuất {len(products)} sản phẩm ra file products_data.json')
    
    # In thống kê
    total_stock = sum(p['stock'] for p in products)
    categories = {}
    for p in products:
        cat = p['category']
        if cat not in categories:
            categories[cat] = {'count': 0, 'stock': 0}
        categories[cat]['count'] += 1
        categories[cat]['stock'] += p['stock']
    
    print(f'\nThống kê:')
    print(f'- Tổng số sản phẩm: {len(products)}')
    print(f'- Tổng tồn kho: {total_stock}')
    print(f'- Theo danh mục:')
    for cat, stats in sorted(categories.items(), key=lambda x: x[1]['stock'], reverse=True):
        print(f'  + {cat}: {stats["count"]} sản phẩm, {stats["stock"]} tồn')
