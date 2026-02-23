"""
Bugungi qo'shilgan mahsulotlarning ortacha narxini qayta hisoblash
"""
import os
from dotenv import load_dotenv
import psycopg2
from decimal import Decimal
from datetime import datetime

load_dotenv()

# Database connection
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    database=os.getenv('DB_NAME', 'sayt_db'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres')
)
cur = conn.cursor()

print('\n=== Bugungi mahsulotlar uchun ortacha narxni qayta hisoblash ===\n')

# Bugungi mahsulotlarni olish (last_batch_date bugungi bo'lganlar)
today = datetime.now().date()

query = '''
    SELECT 
        id, 
        name, 
        cost_price, 
        last_batch_cost, 
        last_batch_date
    FROM products
    WHERE DATE(last_batch_date) = %s 
    AND cost_price = last_batch_cost
    ORDER BY id DESC
'''

cur.execute(query, (today,))
products = cur.fetchall()

print(f'Topildi: {len(products)} ta mahsulot (cost_price = last_batch_cost)\n')

if not products:
    print('✅ Hech qanday muammoli mahsulot topilmadi!')
    cur.close()
    conn.close()
    exit(0)

fixed_count = 0

for prod in products:
    prod_id, prod_name, cost_price, last_batch_cost, last_batch_date = prod
    
    print(f'\n{prod_id}. {prod_name[:60]}')
    print(f'   Hozirgi cost_price: ${float(cost_price):.2f}')
    print(f'   last_batch_cost:    ${float(last_batch_cost):.2f}')
    
    # Barcha joylashuvlardagi miqdorlarni olish
    query_stocks = '''
        SELECT 'warehouse' as type, w.name, ws.quantity
        FROM warehouse_stocks ws
        JOIN warehouses w ON ws.warehouse_id = w.id
        WHERE ws.product_id = %s AND ws.quantity > 0
        UNION ALL
        SELECT 'store' as type, s.name, ss.quantity
        FROM store_stocks ss
        JOIN stores s ON ss.store_id = s.id
        WHERE ss.product_id = %s AND ss.quantity > 0
    '''
    
    cur.execute(query_stocks, (prod_id, prod_id))
    stocks = cur.fetchall()
    
    if not stocks or len(stocks) == 0:
        print('   ⚠️ Stock mavjud emas - o\'zgartirilmaydi')
        continue
    
    # Agar faqat bitta joylashuv bo'lsa - ortacha narx = last_batch_cost
    if len(stocks) == 1:
        print('   ℹ️  Faqat 1 ta joylashuv - ortacha narx to\'g\'ri')
        continue
    
    # Ko'p joylashuv - ortacha narxni hisoblash kerak
    print(f'   📊 {len(stocks)} ta joylashuvda mavjud:')
    
    total_quantity = Decimal('0')
    total_value = Decimal('0')
    
    for stock_type, stock_name, quantity in stocks:
        qty = Decimal(str(quantity))
        # Eski narx bilan hisoblash (last_batch_cost'dan oldingi)
        # Bu yerda biz taxmin qilamiz - eski narx ham shu edi
        value = qty * Decimal(str(cost_price))
        total_quantity += qty
        total_value += value
        print(f'      • {stock_type}: {stock_name} - {float(qty)} ta')
    
    # Yangi ortacha narxni hisoblash
    # Eski qiymat + yangi qo'shilgan
    # Muammo: biz necha ta yangi qo'shilganini bilmaymiz!
    # Shunchaki cost_price ni saqlab qolamiz
    
    print(f'   ⚠️ Ko\'p joylashuv bor, lekin yangi qo\'shilgan miqdor noma\'lum')
    print(f'   💡 Frontend\'da ortacha narx avtomatik hisoblanadi')

print(f'\n\n📊 Xulosa:')
print(f'   Tekshirilgan: {len(products)} ta mahsulot')
print(f'   O\'zgartirilgan: {fixed_count} ta mahsulot')
print(f'\n💡 Frontend\'da tuzatish amalga oshirildi:')
print(f'   ✅ Mahsulot tanlanganida ortacha narx yuborila
di')
print(f'   ✅ Miqdor kiritilganda o\'rtacha narx hisoblanadi')
print(f'   ✅ Backend\'ga ortacha narx va yangi partiya narxi yuboriladi\n')

cur.close()
conn.close()
