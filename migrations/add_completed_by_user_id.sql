-- Add completed_by_user_id column to stock_check_sessions table
-- This column tracks which user completed/finished the stock check session

ALTER TABLE stock_check_sessions 
ADD COLUMN IF NOT EXISTS completed_by_user_id INTEGER REFERENCES users(id);

-- Add index for better query performance
CREATE INDEX IF NOT EXISTS idx_stock_check_sessions_completed_by_user_id 
ON stock_check_sessions(completed_by_user_id);

-- Update existing completed sessions to set completed_by_user_id = user_id (fallback)
UPDATE stock_check_sessions 
SET completed_by_user_id = user_id 
WHERE status = 'completed' AND completed_by_user_id IS NULL;

-- Add comment
COMMENT ON COLUMN stock_check_sessions.completed_by_user_id IS 'ID of user who completed/finished the stock check session';
