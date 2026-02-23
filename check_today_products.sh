#!/bin/bash
# Bugungi mahsulotlarning ortacha narxini qayta hisoblash

echo "Bugungi mahsulotlarni ko'rish..."

sudo -u postgres psql -d sayt_db << 'EOF'
\echo '=== Bugungi qo'\''shilgan mahsulotlar ==='
SELECT 
    id,
    LEFT(name, 50) as mahsulot,
    cost_price as ortacha,
    last_batch_cost as oxirgi,
    CASE 
        WHEN cost_price = last_batch_cost THEN 'TENG (ortacha hisoblanmagan)'
        ELSE 'FARQ BOR (ortacha to''g''ri)'
    END as holat
FROM products
WHERE DATE(last_batch_date) = CURRENT_DATE
ORDER BY id DESC;

\echo ''
\echo '=== Har bir mahsulotning joylashuvlari ==='

DO $$
DECLARE
    prod RECORD;
    w_count INT;
    s_count INT;
    total_count INT;
BEGIN
    FOR prod IN 
        SELECT id, name, cost_price, last_batch_cost
        FROM products 
        WHERE DATE(last_batch_date) = CURRENT_DATE
    LOOP
        SELECT COUNT(*) INTO w_count FROM warehouse_stocks WHERE product_id = prod.id AND quantity > 0;
        SELECT COUNT(*) INTO s_count FROM store_stocks WHERE product_id = prod.id AND quantity > 0;
        total_count := w_count + s_count;
        
        RAISE NOTICE 'ID %: % - % joylashuv (% ombor, % dokon) - Ortacha: $%, Oxirgi: $%',
            prod.id, 
            LEFT(prod.name, 40),
            total_count, 
            w_count, 
            s_count,
            prod.cost_price,
            prod.last_batch_cost;
    END LOOP;
END $$;

EOF

echo ""
echo "Tugadi!"
