import os
from dotenv import load_dotenv
import psycopg2
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

print('\n=== Products jadvalidagi oxirgi 25 ta mahsulot ===\n')

query = '''
    SELECT id, name, cost_price, last_batch_cost, last_batch_date, sell_price
    FROM products
    ORDER BY id DESC
    LIMIT 25
'''

cur.execute(query)
products = cur.fetchall()

problem_count = 0

for prod in products:
    p_id, p_name, p_cost, p_last_batch, p_last_date, p_sell = prod
    p_cost_val = float(p_cost)
    p_last_val = float(p_last_batch) if p_last_batch else 0
    p_sell_val = float(p_sell)
    
    date_str = p_last_date.strftime("%d/%m/%Y %H:%M") if p_last_date else "N/A"
    
    print(f'{p_id}. {p_name[:55]:<57}')
    print(f'   cost_price (ortacha tan narx): ${p_cost_val:.2f}')
    print(f'   last_batch_cost (oxirgi):      ${p_last_val:.2f}')
    print(f'   sell_price:                     ${p_sell_val:.2f}')
    print(f'   Oxirgi qo\'shilgan:              {date_str}')
    
    # Tekshirish - ortacha narx hisoblangan yoki yo'q
    if abs(p_cost_val - p_last_val) < 0.01 and p_last_val > 0:
        print(f'   ⚠️ MUAMMO: cost_price = last_batch_cost')
        print(f'             (O\'rtacha narx HISOBLANMAGAN!)')
        problem_count += 1
    else:
        print(f'   ✅ OK: cost_price va last_batch_cost farq qiladi')
    print()

print(f'\n📊 Natija:')
print(f'   Jami tekshirildi: {len(products)} ta mahsulot')
print(f'   Muammoli:         {problem_count} ta (ortacha narx hisoblanmagan)')
print(f'   To\'g\'ri:           {len(products) - problem_count} ta\n')

cur.close()
conn.close()
