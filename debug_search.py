#!/usr/bin/env python3
"""Debug: Mahsulot qidirishni tekshirish"""
from app import app, db, Product, StoreStock

with app.app_context():
    # 1. Jami mahsulotlar soni
    total = Product.query.count()
    print(f"Jami mahsulotlar: {total}")
    
    # 2. LASETTI qidirish
    results = Product.query.filter(Product.name.ilike('%LASETTI%')).all()
    print(f"\nLASETTI ilike natija: {len(results)}")
    for r in results[:10]:
        print(f"  ID={r.id}, Name={repr(r.name)}, Barcode={r.barcode}")
    
    # 3. GANTEL qidirish
    results2 = Product.query.filter(Product.name.ilike('%GANTEL%')).all()
    print(f"\nGANTEL ilike natija: {len(results2)}")
    for r in results2[:10]:
        print(f"  ID={r.id}, Name={repr(r.name)}, Barcode={r.barcode}")
    
    # 4. StoreStock da RAVON store ni tekshirish
    from sqlalchemy import text
    stores_result = db.session.execute(text("SELECT id, name FROM stores")).fetchall()
    print(f"\nBarcha do'konlar:")
    for s in stores_result:
        print(f"  ID={s[0]}, Name={s[1]}")
        stock_count = StoreStock.query.filter_by(store_id=s[0]).count()
        print(f"    Stock count: {stock_count}")
    
    # 5. Birinchi 5 ta mahsulot nomi
    print(f"\nBirinchi 5 ta mahsulot:")
    first5 = Product.query.limit(5).all()
    for p in first5:
        print(f"  ID={p.id}, Name={repr(p.name)}")
