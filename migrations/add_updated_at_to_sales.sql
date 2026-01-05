-- Sales jadvaliga updated_at ustuni qo'shish
-- Bu ustun qarz to'lash kabi yangilanishlarni tracking qilish uchun

ALTER TABLE sales ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Mavjud ma'lumotlarga created_at ni nusxalash
UPDATE sales SET updated_at = created_at WHERE updated_at IS NULL;

-- Tekshirish
SELECT 
    id, 
    created_at, 
    updated_at,
    CASE 
        WHEN updated_at > created_at + INTERVAL '1 second' THEN 'Yangilangan'
        ELSE 'Yangi'
    END as status
FROM sales 
ORDER BY id DESC 
LIMIT 10;
