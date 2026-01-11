#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test pagination"""

from app import app, StockCheckSession, db

with app.app_context():
    # Test pagination
    pagination = StockCheckSession.query.filter_by(status='completed').order_by(
        StockCheckSession.updated_at.desc()
    ).paginate(page=1, per_page=50, error_out=False)
    
    print(f"Total sessions: {pagination.total}")
    print(f"Total pages: {pagination.pages}")
    print(f"Current page: {pagination.page}")
    print(f"Items on page: {len(pagination.items)}")
    print(f"Has next: {pagination.has_next}")
    print(f"Has prev: {pagination.has_prev}")
    
    if pagination.items:
        print(f"\nFirst session: {pagination.items[0].id} - {pagination.items[0].location_name}")
