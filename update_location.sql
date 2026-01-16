UPDATE sales 
SET 
    location_id = store_id,
    location_type = 'store'
WHERE 
    store_id IS NOT NULL 
    AND (location_id IS NULL OR location_type IS NULL);

SELECT 
    COUNT(*) as total_sales,
    COUNT(location_id) as with_location_id,
    COUNT(location_type) as with_location_type
FROM sales;
