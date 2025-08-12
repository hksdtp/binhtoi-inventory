#!/usr/bin/env python3
"""
Simple HTTP server để chạy app quản lý tồn kho
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if required files exist
    required_files = ['index.html', 'products_data.json']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Thiếu file: {', '.join(missing_files)}")
        print("Vui lòng chạy data_loader.py trước để tạo file products_data.json")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"🚀 Server đang chạy tại: http://localhost:{PORT}")
            print(f"📱 Mở app tại: http://localhost:{PORT}/index.html")
            print("📊 Dữ liệu từ: Ton kho binh.xlsx")
            print("⏹️  Nhấn Ctrl+C để dừng server")
            
            # Tự động mở browser
            try:
                webbrowser.open(f'http://localhost:{PORT}/index.html')
            except:
                pass
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server đã dừng")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {PORT} đã được sử dụng. Thử port khác:")
            print(f"   python3 -m http.server {PORT + 1}")
        else:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
