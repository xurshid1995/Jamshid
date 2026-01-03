#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Barcode ustuni qo'shish migration
Sanasi: 2026-01-03
"""

from app import app, db
from sqlalchemy import text

def run_migration():
    """Barcode ustuni qo'shish"""
    with app.app_context():
        try:
            print("📦 Barcode migration boshlandi...")
            
            # 1. Barcode ustuni qo'shish
            print("1️⃣ Barcode ustuni qo'shilmoqda...")
            db.session.execute(text("""
                ALTER TABLE products 
                ADD COLUMN IF NOT EXISTS barcode VARCHAR(100)
            """))
            
            # 2. Index qo'shish
            print("2️⃣ Index qo'shilmoqda...")
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_products_barcode 
                ON products(barcode)
            """))
            
            # 3. Unique constraint qo'shish (agar mavjud bo'lmasa)
            print("3️⃣ Unique constraint qo'shilmoqda...")
            try:
                db.session.execute(text("""
                    ALTER TABLE products 
                    ADD CONSTRAINT unique_barcode UNIQUE (barcode)
                """))
            except Exception as e:
                if 'already exists' in str(e).lower():
                    print("   ⚠️ Unique constraint allaqachon mavjud")
                else:
                    raise
            
            db.session.commit()
            print("✅ Barcode migration muvaffaqiyatli bajarildi!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration xatosi: {e}")
            raise

if __name__ == '__main__':
    run_migration()
