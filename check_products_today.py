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

# Avval jadval mavjudligini tekshiramiz
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cur.fetchall()
print("Mavjud jadvallar:")
table_names = [t[0] for t in tables]
for table in tables:
    print(f"  - {table[0]}")
print()

# product_add_history jadvali mavjudligini tekshirish
if 'product_add_history' not in table_names:
    print("⚠️ product_add_history jadvali MAVJUD EMAS!")
    print("   Bu muammoning asosiy sababi!\n")
    
    # Jadvalni yaratish
    print("Jadvalni yaratyapmiz...")
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS product_add_history (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(200) NOT NULL,
            cost_price DECIMAL(15, 2) NOT NULL,
            sell_price DECIMAL(15, 2) NOT NULL,
            quantity DECIMAL(15, 3) NOT NULL,
            location_type VARCHAR(20) NOT NULL,
            location_name VARCHAR(200) NOT NULL,
            added_by VARCHAR(100),
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    '''
    cur.execute(create_table_query)
    conn.commit()
    print("✅ product_add_history jadvali yaratildi!\n")

# Bugungi mahsulotlarni olish
today = datetime.now().date()
query = '''
    SELECT 
        product_name, 
        cost_price, 
        quantity,
        location_name,
        added_date
    FROM product_add_history 
    WHERE DATE(added_date) = %s
    ORDER BY added_date DESC
    LIMIT 30
'''

try:
    cur.execute(query, (today,))
except Exception as e:
    print(f"Query xatosi: {e}")
    print("\nOperationHistory jadvalidan ma'lumot olishga harakat qilamiz...")
    
    # OperationHistory jadvalidan qidirish
    query = '''
        SELECT 
            description,
            new_data,
            location_name,
            created_date
        FROM operation_history 
        WHERE DATE(created_date) = %s
        AND operation_type = 'add_product'
        ORDER BY created_date DESC
        LIMIT 30
    '''
    cur.execute(query, (today,))
rows = cur.fetchall()

print(f'\n=== Bugun qoshilgan mahsulotlar ({today}) ===\n')

for row in rows:
    name, cost, qty, loc, added_date = row
    print(f'{name[:40]:<42} | ${float(cost):>6.2f} | {float(qty):>5} ta | {loc[:15]:<17} | {added_date.strftime("%H:%M")}')

print(f'\nJami: {len(rows)} ta\n')

# Bir nechta mahsulot nomlarini tekshirish
if rows:
    print('\n=== Products jadvalidagi ortacha narxlar ===\n')
    
    # Birinchi 8 ta mahsulotni tekshirish
    for i, row in enumerate(rows[:8], 1):
        pname = row[0]
        history_cost = float(row[1])
        
        query2 = '''SELECT cost_price, last_batch_cost FROM products WHERE name = %s'''
        cur.execute(query2, (pname,))
        prod = cur.fetchone()
        
        if prod:
            p_cost, p_last_batch = prod
            p_cost_val = float(p_cost)
            p_last_val = float(p_last_batch) if p_last_batch else 0
            
            print(f'{i}. {pname[:50]}')
            print(f'   History tan narx:         ${history_cost:.2f}')
            print(f'   Products cost_price:      ${p_cost_val:.2f}')
            print(f'   Products last_batch_cost: ${p_last_val:.2f}')
            
            # Tekshirish - ortacha narx hisoblangan yoki yo'q
            if abs(p_cost_val - history_cost) < 0.01:
                print(f'   ⚠️ MUAMMO: Ortacha narx HISOBLANMAGAN! (cost_price = history cost)')
            else:
                print(f'   ✅ Ortacha narx hisoblangan')
            print()

cur.close()
conn.close()
