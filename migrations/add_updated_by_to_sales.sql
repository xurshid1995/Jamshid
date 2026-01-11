-- Qarz to'lovini qabul qilgan foydalanuvchi uchun ustun qo'shish
ALTER TABLE sales ADD COLUMN IF NOT EXISTS updated_by VARCHAR(100);

-- Eski ma'lumotlar uchun default qiymat
UPDATE sales SET updated_by = created_by WHERE updated_by IS NULL;
