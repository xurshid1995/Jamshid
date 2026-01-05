#!/usr/bin/env python3
"""
Migration: Sales jadvaliga updated_at ustuni qo'shish
"""

from app import app, db
from sqlalchemy import text

def run_migration():
    with app.app_context():
        print("🟡 Migration boshlandi: updated_at ustuni qo'shish...")
        
        try:
            # 1. Ustun qo'shish
            print("\n🔵 1. updated_at ustuni qo'shilmoqda...")
            db.session.execute(text("ALTER TABLE sales ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
            db.session.commit()
            print("   ✅ Ustun qo'shildi")
            
            # 2. Mavjud ma'lumotlarni yangilash
            print("\n🔵 2. Mavjud ma'lumotlar yangilanmoqda...")
            result = db.session.execute(text("UPDATE sales SET updated_at = created_at WHERE updated_at IS NULL"))
            db.session.commit()
            print(f"   ✅ {result.rowcount} ta qator yangilandi")
            
            # 3. Tekshirish
            print("\n🔵 3. Tekshirish...")
            result = db.session.execute(text("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN updated_at IS NOT NULL THEN 1 ELSE 0 END) as with_updated_at
                FROM sales
            """))
            row = result.fetchone()
            print(f"   Jami savdolar: {row[0]}")
            print(f"   updated_at bor: {row[1]}")
            
            print("\n✅ Migration yakunlandi!")
            
        except Exception as e:
            print(f"\n❌ Xatolik: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    run_migration()
