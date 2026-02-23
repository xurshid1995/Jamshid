#!/bin/bash

echo "=== Ortacha narx farq qiladigan mahsulotlar ==="

sudo -u postgres psql -d sayt_db << 'EOF'
SELECT 
    p.id, 
    LEFT(p.name, 40) as mahsulot,
    p.cost_price as ortacha, 
    p.last_batch_cost as oxirgi,
    (SELECT COUNT(*) FROM warehouse_stocks ws WHERE ws.product_id = p.id AND ws.quantity > 0) + 
    (SELECT COUNT(*) FROM store_stocks ss WHERE ss.product_id = p.id AND ss.quantity > 0) as joylashuv
FROM products p 
WHERE DATE(p.last_batch_date) = CURRENT_DATE 
AND p.cost_price != p.last_batch_cost 
ORDER BY p.id DESC;
EOF
