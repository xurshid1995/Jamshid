-- Error logs jadvali - xatoliklarni saqlash uchun
CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    level VARCHAR(20) DEFAULT 'ERROR',
    message TEXT NOT NULL,
    traceback TEXT,
    endpoint VARCHAR(200),
    method VARCHAR(10),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    ip_address VARCHAR(50)
);

-- Index'lar - tezkor qidirish uchun
CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_error_logs_level ON error_logs(level);
CREATE INDEX IF NOT EXISTS idx_error_logs_user_id ON error_logs(user_id);

-- Komment
COMMENT ON TABLE error_logs IS 'Application xatoliklarini saqlash uchun jadval';
COMMENT ON COLUMN error_logs.timestamp IS 'Xatolik vaqti';
COMMENT ON COLUMN error_logs.level IS 'ERROR, WARNING, CRITICAL';
COMMENT ON COLUMN error_logs.message IS 'Xatolik xabari';
COMMENT ON COLUMN error_logs.traceback IS 'Python traceback';
COMMENT ON COLUMN error_logs.endpoint IS 'Flask route';
COMMENT ON COLUMN error_logs.method IS 'HTTP method (GET, POST, etc)';
COMMENT ON COLUMN error_logs.user_id IS 'Xatolik qilgan foydalanuvchi';
COMMENT ON COLUMN error_logs.ip_address IS 'Client IP manzili';
