SELECT id, location_id, location_type, store_id, total_amount, sale_date 
FROM sales 
WHERE sale_date >= CURRENT_DATE 
ORDER BY id DESC 
LIMIT 10;
