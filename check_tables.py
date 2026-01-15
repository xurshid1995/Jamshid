#!/usr/bin/env python3
"""Check database table names"""
from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    print("=" * 60)
    print("DATABASE TABLES:")
    print("=" * 60)
    for table in sorted(tables):
        print(f"  • {table}")
    print("=" * 60)
