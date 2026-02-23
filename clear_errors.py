#!/usr/bin/env python3
"""Database'dagi error_logs jadvalini tozalash"""

from app import app, db, ErrorLog

with app.app_context():
    # Xatoliklar sonini hisoblash
    count = ErrorLog.query.count()
    print(f"📊 Jami xatoliklar soni: {count}")
    
    if count > 0:
        # Barcha xatoliklarni o'chirish
        ErrorLog.query.delete()
        db.session.commit()
        print(f"✅ {count} ta xatolik o'chirildi!")
    else:
        print("ℹ️  Xatoliklar yo'q")
