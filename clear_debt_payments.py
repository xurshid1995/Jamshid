"""
Debt payments jadvalidagi barcha yozuvlarni o'chirish
DIQQAT: Bu qaytarib bo'lmaydigan amal!
"""
from app import app, db, DebtPayment

def clear_debt_payments():
    with app.app_context():
        try:
            # Avval hozirgi holatni ko'rish
            count_before = DebtPayment.query.count()
            print(f"📊 Hozirgi to'lovlar soni: {count_before}")
            
            if count_before == 0:
                print("ℹ️  Jadval allaqachon bo'sh")
                return
            
            # Tasdiqlash
            print(f"⚠️  DIQQAT: {count_before} ta to'lov yozuvi o'chiriladi!")
            print("❓ Davom etish uchun 'ha' deb yozing:")
            
            # Barcha yozuvlarni o'chirish
            deleted = DebtPayment.query.delete()
            db.session.commit()
            
            print(f"✅ {deleted} ta to'lov yozuvi muvaffaqiyatli o'chirildi!")
            
            # Natijani tekshirish
            count_after = DebtPayment.query.count()
            print(f"📊 Qolgan to'lovlar: {count_after}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Xatolik: {str(e)}")
            raise

if __name__ == '__main__':
    print("=" * 60)
    print("🗑️  DEBT PAYMENTS JADVALINI TOZALASH")
    print("=" * 60)
    clear_debt_payments()
