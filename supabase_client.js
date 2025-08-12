/**
 * Supabase client cho frontend
 */

class SupabaseManager {
    constructor() {
        this.supabaseUrl = 'https://zgrfqkytbmahxcbgpkxx.supabase.co';
        this.supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpncmZxa3l0Ym1haHhjYmdwa3h4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxNjI1MTAsImV4cCI6MjA2MTczODUxMH0.a6giZZFMrj6jBhLip3ShOFCyTHt5dbe31UDGCECh0Zs';
        this.supabase = null;
        this.isOnline = navigator.onLine;
        
        // Lắng nghe trạng thái online/offline
        window.addEventListener('online', () => {
            this.isOnline = true;
            console.log('🌐 Đã kết nối internet');
        });
        
        window.addEventListener('offline', () => {
            this.isOnline = false;
            console.log('📡 Mất kết nối internet - chuyển sang chế độ offline');
        });
    }

    async init() {
        if (this.supabaseUrl === 'YOUR_SUPABASE_URL') {
            console.warn('⚠️ Chưa cấu hình Supabase URL - chạy ở chế độ offline');
            return false;
        }

        try {
            // Import Supabase từ CDN
            const { createClient } = window.supabase || {};
            if (!createClient) {
                console.error('❌ Không thể load Supabase library');
                return false;
            }

            this.supabase = createClient(this.supabaseUrl, this.supabaseKey);
            console.log('✅ Đã kết nối Supabase');
            return true;
        } catch (error) {
            console.error('❌ Lỗi khởi tạo Supabase:', error);
            return false;
        }
    }

    async loadProducts() {
        if (!this.isOnline || !this.supabase) {
            return this.loadLocalProducts();
        }

        try {
            const { data, error } = await this.supabase
                .from('products')
                .select('*')
                .order('id');

            if (error) {
                console.error('❌ Lỗi tải dữ liệu từ Supabase:', error);
                return this.loadLocalProducts();
            }

            // Lưu cache local
            localStorage.setItem('products_cache', JSON.stringify(data));
            localStorage.setItem('cache_timestamp', Date.now().toString());
            
            console.log(`✅ Tải ${data.length} sản phẩm từ Supabase`);
            return data;

        } catch (error) {
            console.error('❌ Lỗi kết nối Supabase:', error);
            return this.loadLocalProducts();
        }
    }

    loadLocalProducts() {
        try {
            // Thử cache trước
            const cache = localStorage.getItem('products_cache');
            if (cache) {
                console.log('📦 Sử dụng dữ liệu cache');
                return JSON.parse(cache);
            }

            // Fallback về file JSON
            return fetch('/products_data.json')
                .then(response => response.json())
                .then(data => {
                    console.log('📄 Tải dữ liệu từ file local');
                    return data;
                })
                .catch(error => {
                    console.error('❌ Lỗi tải dữ liệu local:', error);
                    return [];
                });

        } catch (error) {
            console.error('❌ Lỗi đọc cache:', error);
            return [];
        }
    }

    async updateStock(productId, newStock) {
        if (!this.isOnline || !this.supabase) {
            console.warn('📡 Offline - không thể cập nhật stock');
            return false;
        }

        try {
            const { data, error } = await this.supabase
                .from('products')
                .update({ stock: newStock, updated_at: new Date().toISOString() })
                .eq('id', productId)
                .select();

            if (error) {
                console.error('❌ Lỗi cập nhật stock:', error);
                return false;
            }

            console.log('✅ Đã cập nhật stock:', data[0]);
            
            // Cập nhật cache local
            this.updateLocalCache(productId, { stock: newStock });
            return true;

        } catch (error) {
            console.error('❌ Lỗi cập nhật stock:', error);
            return false;
        }
    }

    updateLocalCache(productId, updates) {
        try {
            const cache = localStorage.getItem('products_cache');
            if (cache) {
                const products = JSON.parse(cache);
                const productIndex = products.findIndex(p => p.id === productId);
                
                if (productIndex !== -1) {
                    products[productIndex] = { ...products[productIndex], ...updates };
                    localStorage.setItem('products_cache', JSON.stringify(products));
                }
            }
        } catch (error) {
            console.error('❌ Lỗi cập nhật cache:', error);
        }
    }

    async syncData() {
        if (!this.isOnline || !this.supabase) {
            console.warn('📡 Không thể sync - offline hoặc chưa cấu hình Supabase');
            return false;
        }

        try {
            const data = await this.loadProducts();
            console.log('🔄 Đã sync dữ liệu với Supabase');
            return data;
        } catch (error) {
            console.error('❌ Lỗi sync dữ liệu:', error);
            return false;
        }
    }

    getConnectionStatus() {
        return {
            online: this.isOnline,
            supabaseReady: !!this.supabase,
            hasCache: !!localStorage.getItem('products_cache')
        };
    }
}

// Khởi tạo global instance
window.supabaseManager = new SupabaseManager();