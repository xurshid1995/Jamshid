-- Qoldiq tekshirish sessiyalari jadvali
CREATE TABLE IF NOT EXISTS stock_check_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL,
    location_type VARCHAR(20) NOT NULL CHECK (location_type IN ('store', 'warehouse')),
    location_name VARCHAR(255) NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled')),
    
    -- Bir joylashuv bir vaqtda faqat bir foydalanuvchi tomonidan tekshirilishi mumkin
    CONSTRAINT unique_active_location UNIQUE (location_id, location_type, status)
);

-- Index'lar yaratish (tezroq qidirish uchun)
CREATE INDEX idx_stock_sessions_user ON stock_check_sessions(user_id);
CREATE INDEX idx_stock_sessions_location ON stock_check_sessions(location_id, location_type);
CREATE INDEX idx_stock_sessions_status ON stock_check_sessions(status);
CREATE INDEX idx_stock_sessions_updated ON stock_check_sessions(updated_at);

-- Comment qo'shish
COMMENT ON TABLE stock_check_sessions IS 'Qoldiq tekshirish sessiyalarini kuzatish - bir vaqtda bir joylashuvni faqat bitta foydalanuvchi tekshirishi mumkin';
COMMENT ON COLUMN stock_check_sessions.location_type IS 'store yoki warehouse';
COMMENT ON COLUMN stock_check_sessions.status IS 'active (tekshirilmoqda), completed (tugallangan), cancelled (bekor qilingan)';
