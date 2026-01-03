-- Mahsulot jadvaliga barcode ustuni qo'shish
-- Sanasi: 2026-01-03

ALTER TABLE products 
ADD COLUMN IF NOT EXISTS barcode VARCHAR(100);

-- Barcode ustuniga index qo'shish (tezkor qidiruv uchun)
CREATE INDEX IF NOT EXISTS idx_products_barcode ON products(barcode);

-- Barcode unique bo'lishi shart (duplikat bo'lmasin)
ALTER TABLE products 
ADD CONSTRAINT unique_barcode UNIQUE (barcode);

-- Izoh: Barcode bo'sh bo'lishi mumkin, lekin agar mavjud bo'lsa unique bo'lishi kerak
