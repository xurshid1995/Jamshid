SELECT id, location_id, location_type, store_id, total_amount, sale_date 
FROM sales 
WHERE location_type = 'warehouse' 
ORDER BY id DESC 
LIMIT 5;
