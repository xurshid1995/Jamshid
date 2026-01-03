#!/usr/bin/env python3
"""
NULL product_id li transferlarni tozalash va keyin yetim mahsulotlarni o'chirish
"""

from app import app, db, Product, StoreStock, WarehouseStock, Transfer
from sqlalchemy import and_, not_, exists

def clean_all():
    """NULL transferlar va yetim mahsulotlarni tozalash"""
    with app.app_context():
        # 1. NULL product_id li transferlarni o'chirish
        null_transfers = Transfer.query.filter(Transfer.product_id == None).all()
        if null_transfers:
            print(f"\n⚠️  {len(null_transfers)} ta NULL product_id li transfer topildi")
            for transfer in null_transfers:
                db.session.delete(transfer)
            db.session.commit()
            print(f"✅ {len(null_transfers)} ta NULL transfer o'chirildi\n")
        else:
            print("✅ NULL transferlar yo'q\n")
        
        # 2. Yetim mahsulotlarni topish
        orphan_products = Product.query.filter(
            and_(
                not_(exists().where(StoreStock.product_id == Product.id)),
                not_(exists().where(WarehouseStock.product_id == Product.id))
            )
        ).all()
        
        if not orphan_products:
            print("✅ Yetim mahsulotlar yo'q!")
            return
        
        print(f"⚠️  {len(orphan_products)} ta yetim mahsulot topildi")
        print("Bu mahsulotlar o'chiriladi...\n")
        
        # 3. O'chirish
        deleted_count = 0
        for product in orphan_products:
            # Ushbu mahsulotga tegishli transferlarni ham o'chirish
            product_transfers = Transfer.query.filter_by(product_id=product.id).all()
            for transfer in product_transfers:
                db.session.delete(transfer)
                deleted_count += 1
            
            db.session.delete(product)
        
        db.session.commit()
        print(f"✅ {len(orphan_products)} ta yetim mahsulot o'chirildi!")
        if deleted_count > 0:
            print(f"✅ {deleted_count} ta tegishli transfer ham o'chirildi!")

if __name__ == '__main__':
    clean_all()
