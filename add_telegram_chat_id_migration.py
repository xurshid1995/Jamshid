# -*- coding: utf-8 -*-
"""
Migration: Customer jadvaliga telegram_chat_id ustunini qo'shish
"""
import os
import sys
from dotenv import load_dotenv

# Flask app va db ni import qilish
sys.path.append(os.path.dirname(__file__))
load_dotenv()

def run_migration():
    """Migration ni bajarish"""
    from app import app, db
    
    with app.app_context():
        try:
            # telegram_chat_id ustunini qo'shish
            sql = """
            -- Customer jadvaliga telegram_chat_id ustunini qo'shish
            ALTER TABLE customers 
            ADD COLUMN IF NOT EXISTS telegram_chat_id BIGINT;
            
            -- Index yaratish (tez qidiruv uchun)
            CREATE INDEX IF NOT EXISTS idx_customers_telegram_chat_id 
            ON customers(telegram_chat_id);
            
            -- Comment qo'shish
            COMMENT ON COLUMN customers.telegram_chat_id IS 
            'Mijozning Telegram chat ID si (bot bilan muloqot uchun)';
            """
            
            print("📝 Migration boshlanmoqda...")
            db.session.execute(db.text(sql))
            db.session.commit()
            print("✅ Migration muvaffaqiyatli bajarildi!")
            print("✅ customers.telegram_chat_id ustuni qo'shildi")
            print("✅ Index yaratildi: idx_customers_telegram_chat_id")
            
            # Tekshirish
            result = db.session.execute(db.text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'customers' 
                AND column_name = 'telegram_chat_id'
            """))
            
            row = result.fetchone()
            if row:
                print(f"\n✅ Ustun muvaffaqiyatli yaratildi:")
                print(f"   Ustun: {row[0]}")
                print(f"   Tur: {row[1]}")
            else:
                print("\n⚠️ Ustun topilmadi")
            
        except Exception as e:
            print(f"❌ Migration xatosi: {e}")
            db.session.rollback()
            raise

def rollback_migration():
    """Migration ni bekor qilish"""
    from app import app, db
    
    with app.app_context():
        try:
            sql = """
            -- Index o'chirish
            DROP INDEX IF EXISTS idx_customers_telegram_chat_id;
            
            -- Ustunni o'chirish
            ALTER TABLE customers 
            DROP COLUMN IF EXISTS telegram_chat_id;
            """
            
            print("🔄 Rollback boshlanmoqda...")
            db.session.execute(db.text(sql))
            db.session.commit()
            print("✅ Rollback muvaffaqiyatli bajarildi!")
            
        except Exception as e:
            print(f"❌ Rollback xatosi: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Customer telegram_chat_id migration')
    parser.add_argument(
        '--rollback',
        action='store_true',
        help='Rollback migration (o\'chirish)'
    )
    
    args = parser.parse_args()
    
    if args.rollback:
        print("⚠️ Migration bekor qilinmoqda...")
        confirm = input("Davom ettirasizmi? (yes/no): ")
        if confirm.lower() == 'yes':
            rollback_migration()
        else:
            print("❌ Bekor qilindi")
    else:
        run_migration()
