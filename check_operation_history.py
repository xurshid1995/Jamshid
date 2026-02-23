import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import json

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

# Bugungi operation_history dan mahsulot qo'shish operatsiyalarini olish
today = datetime.now().date()
query = '''
    SELECT 
        id,
        description,
        new_data,
        location_name,
        username,
        created_date
    FROM operation_history 
    WHERE DATE(created_date) = %s
    AND operation_type = 'add_product'
    ORDER BY created_date DESC
    LIMIT 30
'''

cur.execute(query, (today,))
rows = cur.fetchall()

print(f'\n=== Bugun qoshilgan mahsulotlar (operation_history) - {today} ===\n')

if not rows:
    print("⚠️ Bugun hech qanday mahsulot qo'shilmagan yoki operation_history'ga yozilmagan\n")
else:
    for row in rows:
        op_id, description, new_data_str, loc_name, username, created_date = row
        
        # JSON parse qilish
        try:
            new_data = json.loads(new_data_str) if new_data_str else {}
            product_name = new_data.get('product_name', 'N/A')
            cost_price = new_data.get('cost_price', 0)
            sell_price = new_data.get('sell_price', 0)
            quantity = new_data.get('quantity', 0)
            
            print(f'{created_date.strftime("%H:%M")} | {product_name[:40]:<42}')
            print(f'       Tan: ${cost_price:>6.2f} | Sot: ${sell_price:>6.2f} | {quantity:>5} ta | {loc_name[:20]:<22} | {username}')
            print()
        except Exception as e:
            print(f'{created_date.strftime("%H:%M")} | {description}')
            print(f'       Parse xatosi: {e}')
            print()

print(f'Jami: {len(rows)} ta operatsiya\n')

# Endi products jadvalidan ma'lumot olish
print('=== Products jadvalidagi bir nechta mahsulot ===\n')

query2 = '''
    SELECT id, name, cost_price, last_batch_cost, last_batch_date
    FROM products
    ORDER BY id DESC
    LIMIT 10
'''

cur.execute(query2)
products = cur.fetchall()

for prod in products:
    p_id, p_name, p_cost, p_last_batch, p_last_date = prod
    p_cost_val = float(p_cost)
    p_last_val = float(p_last_batch) if p_last_batch else 0
    
    print(f'{p_id}. {p_name[:50]}')
    print(f'   cost_price (ortacha):      ${p_cost_val:.2f}')
    print(f'   last_batch_cost:           ${p_last_val:.2f}')
    
    # Tekshirish - ortacha narx hisoblangan yoki yo'q
    if abs(p_cost_val - p_last_val) < 0.01:
        print(f'   ⚠️ SHUBHALI: cost_price = last_batch_cost (ortacha hisoblanmagan bo\'lishi mumkin)')
    else:
        print(f'   ✅ cost_price != last_batch_cost (ortacha boshqacha)')
    print()

cur.close()
conn.close()
