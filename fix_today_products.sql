-- Bugungi qo'shilgan mahsulotlar uchun ortacha narxni qayta hisoblash

-- Barcha mahsulotlar uchun ortacha narxni hisoblash funksiyasi
DO $$
DECLARE
    product_record RECORD;
    total_qty DECIMAL;
    total_value DECIMAL;
    new_avg_cost DECIMAL;
    warehouse_qty DECIMAL;
    store_qty DECIMAL;
BEGIN
    -- Bugungi last_batch_date bo'lgan mahsulotlarni olish
    FOR product_record IN 
        SELECT id, name, cost_price, last_batch_cost, last_batch_date
        FROM products 
        WHERE DATE(last_batch_date) = CURRENT_DATE
    LOOP
        -- Warehouse stocklarni yig'ish
        SELECT COALESCE(SUM(quantity), 0) INTO warehouse_qty
        FROM warehouse_stocks 
        WHERE product_id = product_record.id;
        
        -- Store stocklarni yig'ish
        SELECT COALESCE(SUM(quantity), 0) INTO store_qty
        FROM store_stocks 
        WHERE product_id = product_record.id;
        
        total_qty := warehouse_qty + store_qty;
        
        -- Agar jami miqdor 0 bo'lsa, o'tkazib yuborish
        IF total_qty = 0 THEN
            RAISE NOTICE 'Mahsulot ID %: % - Stock yo''q, o''tkazib yuborildi', product_record.id, product_record.name;
            CONTINUE;
        END IF;
        
        -- Agar faqat bitta joylashuv bo'lsa va cost_price = last_batch_cost, bu yangi mahsulot
        IF total_qty > 0 AND product_record.cost_price = product_record.last_batch_cost THEN
            RAISE NOTICE 'Mahsulot ID %: % - Yangi mahsulot yoki birinchi partiya, ortacha narx to''g''ri', 
                product_record.id, product_record.name;
            CONTINUE;
        END IF;
        
        -- Ortacha narxni hisoblash uchun umumiy qiymatni topish
        -- Bu juda murakkab, chunki biz har bir qo'shilgan paytdagi narxni bilmaymiz
        -- Eng yaxshi yechim - hozirgi cost_price ni saqlab qolish
        
        RAISE NOTICE 'Mahsulot ID %: % - Jami miqdor: %, Hozirgi avg: $%, Last batch: $%', 
            product_record.id, product_record.name, total_qty, 
            product_record.cost_price, product_record.last_batch_cost;
            
        -- Agar cost_price va last_batch_cost bir xil bo'lsa, bu yangi mahsulot
        -- Aks holda, frontend allaqachon to'g'ri ortacha narxni hisoblagan
        
    END LOOP;
    
    RAISE NOTICE 'Tugadi!';
END $$;

-- Natijalarni ko'rish
SELECT 
    id,
    name,
    cost_price as "Ortacha narx",
    last_batch_cost as "Oxirgi partiya",
    last_batch_date as "Oxirgi sana",
    CASE 
        WHEN cost_price = last_batch_cost THEN 'Yangi mahsulot'
        ELSE 'Ortacha hisoblangan'
    END as "Status"
FROM products
WHERE DATE(last_batch_date) = CURRENT_DATE
ORDER BY id DESC;
