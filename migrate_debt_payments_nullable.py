"""
Migration: DebtPayment jadvalida customer_id ni nullable qilish
"""
from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("🔄 Migratsiya boshlanmoqda...")
            
            # 1. customer_id NULL bo'lishiga ruxsat berish
            print("📝 customer_id columnni nullable qilish...")
            db.session.execute(text("""
                ALTER TABLE debt_payments 
                ALTER COLUMN customer_id DROP NOT NULL;
            """))
            
            # 2. Foreign key constraint ni o'zgartirish (agar mavjud bo'lsa)
            print("🔗 Foreign key constraint ni SET NULL qilish...")
            
            # Avval eski constraint nomini topamiz
            result = db.session.execute(text("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'debt_payments' 
                AND constraint_type = 'FOREIGN KEY'
                AND constraint_name LIKE '%customer%';
            """))
            
            constraints = result.fetchall()
            for constraint in constraints:
                constraint_name = constraint[0]
                print(f"   🗑️ O'chirilmoqda: {constraint_name}")
                db.session.execute(text(f"""
                    ALTER TABLE debt_payments 
                    DROP CONSTRAINT IF EXISTS {constraint_name};
                """))
            
            # Yangi constraint qo'shamiz - SET NULL bilan
            print("   ➕ Yangi constraint qo'shilmoqda (ON DELETE SET NULL)...")
            db.session.execute(text("""
                ALTER TABLE debt_payments 
                ADD CONSTRAINT debt_payments_customer_id_fkey 
                FOREIGN KEY (customer_id) 
                REFERENCES customers(id) 
                ON DELETE SET NULL;
            """))
            
            db.session.commit()
            print("✅ Migratsiya muvaffaqiyatli yakunlandi!")
            print("ℹ️  Endi mijoz o'chirilganda debt_payments yozuvlari saqlanadi, faqat customer_id NULL bo'ladi")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Xatolik: {str(e)}")
            raise

if __name__ == '__main__':
    migrate()
