UPDATE sales 
SET location_id = store_id, location_type = 'store' 
WHERE id = 249;

SELECT id, location_id, location_type, store_id FROM sales ORDER BY id;
