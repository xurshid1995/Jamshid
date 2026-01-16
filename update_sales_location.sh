"""
Migration: Update existing sales with location_id and location_type
Bu script eski savdolarda location_id va location_type ustunlarini to'ldiradi
"""

# Database'ga ulanish
ssh root@139.59.154.185 "sudo -u postgres psql -d sayt_db -c \"
UPDATE sales 
SET 
    location_id = store_id,
    location_type = 'store'
WHERE 
    store_id IS NOT NULL 
    AND (location_id IS NULL OR location_type IS NULL);
\""

# Natijani tekshirish
ssh root@139.59.154.185 "sudo -u postgres psql -d sayt_db -c \"
SELECT 
    COUNT(*) as total_sales,
    COUNT(location_id) as with_location_id,
    COUNT(location_type) as with_location_type
FROM sales;
\""
