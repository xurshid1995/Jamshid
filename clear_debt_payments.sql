-- Debt payments jadvalidagi barcha yozuvlarni o'chirish
-- DIQQAT: Bu amal qaytarib bo'lmaydi!

-- Avval hozirgi holatni ko'rish
SELECT COUNT(*) as total_payments FROM debt_payments;

-- Barcha yozuvlarni o'chirish
TRUNCATE TABLE debt_payments RESTART IDENTITY CASCADE;

-- Natijani tekshirish
SELECT COUNT(*) as total_payments_after FROM debt_payments;
