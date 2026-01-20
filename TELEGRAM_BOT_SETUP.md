# 📱 Telegram Bot - Qarz Eslatmalari Tizimi

Mijozlarga qarzlarini avtomatik ravishda Telegram orqali yuborish tizimi.

## 📋 Tizim imkoniyatlari

### ✅ Asosiy funksiyalar:
- 🔔 **Kunlik avtomatik eslatmalar** - har kuni belgilangan vaqtda
- 📊 **Haftalik hisobotlar** - adminlarga qarzlar statistikasi
- ⚡ **Real-time xabarlar** - savdodan keyin darhol eslatma
- ✅ **To'lov tasdiqlash** - qarz to'langanda xabar yuborish
- 👤 **Mijoz botdan foydalanishi** - qarzni tekshirish

### 📈 Tizim arxitekturasi:

```
┌─────────────────────────────────┐
│   PostgreSQL Database           │
│   - customers (telegram_chat_id)│
│   - sales (debt_amount)         │
└──────────────┬──────────────────┘
               │
        ┌──────▼────────┐
        │  Flask App    │
        │  (app.py)     │
        └──────┬────────┘
               │
    ┌──────────▼────────────┐
    │  Debt Scheduler       │
    │  - Kunlik tekshirish  │
    │  - Avtomatik yuborish │
    └──────────┬────────────┘
               │
    ┌──────────▼────────────┐
    │   Telegram Bot        │
    │   - Xabar yuborish    │
    │   - Formatlar         │
    └───────────────────────┘
```

## 🚀 O'rnatish va sozlash

### 1. Telegram Bot yaratish

1. Telegram'da **@BotFather** ni qidiring
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: "Qarz Eslatmasi Bot")
4. Bot username kiriting (masalan: "qarz_eslatma_bot")
5. BotFather sizga **token** beradi
6. Bu tokenni saqlang!

### 2. Chat ID olish

Admin hisobotlarini qabul qilish uchun:

1. Telegram'da **@userinfobot** ni qidiring
2. `/start` yuboring
3. Bot sizga **chat ID** ni beradi (masalan: 123456789)
4. Bu ID ni saqlang!

### 3. Dependencies o'rnatish

```bash
# Virtual environment yaratish (ixtiyoriy)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Paketlarni o'rnatish
pip install -r requirements.txt
```

Yangi paketlar:
- `python-telegram-bot==20.7` - Telegram bot API
- `apscheduler==3.10.4` - Avtomatik vazifalar

### 4. .env faylni sozlash

`.env` faylingizga quyidagilarni qo'shing:

```env
# ============================================
# TELEGRAM BOT SOZLAMALARI
# ============================================

# Bot token (BotFather dan)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Admin chat IDs (vergul bilan ajratilgan)
TELEGRAM_ADMIN_CHAT_IDS=123456789,987654321

# Kunlik eslatmalar vaqti (HH:MM)
DEBT_REMINDER_TIME=10:00

# Haftalik hisobot kuni (0=Yakshanba, 1=Dushanba, ...)
WEEKLY_REPORT_DAY=1

# Minimal qarz miqdori (USD)
MINIMUM_DEBT_AMOUNT=1.0
```

### 5. Database migration

Customer jadvaliga `telegram_chat_id` ustunini qo'shish:

```bash
python add_telegram_chat_id_migration.py
```

Natija:
```
✅ Migration muvaffaqiyatli bajarildi!
✅ customers.telegram_chat_id ustuni qo'shildi
✅ Index yaratildi: idx_customers_telegram_chat_id
```

### 6. Mijozlarga Telegram Chat ID qo'shish

Mijozlar ma'lumotlarini tahrirlashda `telegram_chat_id` ni kiriting:

**Variant 1: Qo'lda kiritish**
- Mijoz profilida "Telegram Chat ID" maydoniga ID ni kiriting
- Mijoz o'zi botga `/start` yuborganda ID ni ko'rsatadi

**Variant 2: Avtomatik (bot orqali)**
```python
# Bot commandida:
# Mijoz /start yuborganda
chat_id = update.effective_chat.id
phone = update.message.contact.phone_number  # Agar telefon yuborsa

# Database'da yangilash
customer = Customer.query.filter_by(phone=phone).first()
if customer:
    customer.telegram_chat_id = chat_id
    db.session.commit()
```

## 🎯 Qanday ishlatish

### Flask app bilan birgalikda

Flask app avtomatik ravishda bot scheduler ni ishga tushiradi:

```bash
python app.py
```

Konsolda ko'rasiz:
```
🤖 Telegram bot scheduler ishga tushirilmoqda...
✅ Telegram bot muvaffaqiyatli ishga tushdi
✅ Kunlik eslatmalar: har kuni 10:00 da
✅ Haftalik hisobot: har dushanba 09:00 da
✅ Scheduler ishga tushdi
```

### Alohida test qilish

**1. Bot test (xabar yuborish):**

```python
# telegram_bot.py
import asyncio
from telegram_bot import get_bot_instance

async def test():
    bot = get_bot_instance()
    
    # Test xabar
    await bot.send_debt_reminder(
        chat_id=123456789,  # O'z chat ID ingiz
        customer_name="Test Mijoz",
        debt_usd=150.50,
        debt_uzs=1956500,
        location_name="Test Do'kon"
    )

asyncio.run(test())
```

**2. Scheduler test:**

```python
# Test script
from app import app, db
from debt_scheduler import get_scheduler_instance
import asyncio

# Scheduler yaratish
scheduler = get_scheduler_instance(app, db)

# Darhol eslatma yuborish
asyncio.run(
    scheduler.send_instant_reminder(
        customer_id=1,
        debt_usd=100,
        debt_uzs=1300000,
        location_name="Test Do'kon"
    )
)
```

## 💡 Kod integratsiyasi

### Savdodan keyin avtomatik eslatma

`app.py` dagi savdo funksiyasiga qo'shing:

```python
from debt_scheduler import get_scheduler_instance
import asyncio

@app.route('/api/sales', methods=['POST'])
def create_sale():
    # ... mavjud kod ...
    
    # Agar qarz bo'lsa, Telegram eslatmasi yuborish
    if payment_status == 'partial' and debt_usd > 0:
        try:
            scheduler = get_scheduler_instance(app, db)
            
            # Async funksiyani ishga tushirish
            asyncio.run(
                scheduler.send_instant_reminder(
                    customer_id=customer_id,
                    debt_usd=float(debt_usd),
                    debt_uzs=float(debt_uzs),
                    location_name=location_name
                )
            )
            logger.info(f"✅ Telegram eslatmasi yuborildi: {customer_name}")
        except Exception as e:
            logger.error(f"❌ Telegram eslatmasi yuborishda xatolik: {e}")
    
    # ... davom etadi ...
```

### Qarz to'langanda tasdiq xabari

```python
@app.route('/api/debt_payment', methods=['POST'])
def debt_payment():
    # ... mavjud kod ...
    
    # To'lov tasdiq xabarini yuborish
    try:
        scheduler = get_scheduler_instance(app, db)
        
        asyncio.run(
            scheduler.send_payment_notification(
                customer_id=customer_id,
                paid_usd=float(paid_usd),
                paid_uzs=float(paid_uzs),
                remaining_usd=float(remaining_usd),
                remaining_uzs=float(remaining_uzs),
                location_name=location_name
            )
        )
        logger.info(f"✅ To'lov tasdiq xabari yuborildi")
    except Exception as e:
        logger.error(f"❌ To'lov tasdiq xabarida xatolik: {e}")
    
    # ... davom etadi ...
```

## 📊 Bot sozlamalari

### Eslatmalar vaqtini o'zgartirish

`.env` faylda:
```env
DEBT_REMINDER_TIME=14:30  # 14:30 ga o'zgartirish
```

### Haftalik hisobot kunini o'zgartirish

```env
WEEKLY_REPORT_DAY=5  # Juma
# 0=Yakshanba, 1=Dushanba, 2=Seshanba, 3=Chorshanba, 
# 4=Payshanba, 5=Juma, 6=Shanba
```

### Minimal qarz chegarasini o'zgartirish

```env
MINIMUM_DEBT_AMOUNT=5.0  # $5 dan kam qarzlar eslatilmaydi
```

## 🎨 Xabar formatlari

### Qarz eslatmasi:
```
💰 QARZ ESLATMASI

Hurmatli Akmal Karimov!

📍 Joylashuv: Ravon Do'kon
💵 Qarz: $150.50
💸 Qarz: 1,956,500 so'm
📅 Savdo sanasi: 20.01.2026

Iltimos, qarzingizni to'lashni unutmang.
Rahmat! 🙏
```

### To'lov tasdiq xabari:
```
✅ TO'LOV QABUL QILINDI

Hurmatli Akmal Karimov!

📍 Joylashuv: Ravon Do'kon
💵 To'langan: $50.00
💸 To'langan: 650,000 so'm

📊 Qolgan qarz:
💵 $100.50
💸 1,306,500 so'm

Rahmat! 🙏
```

### Adminlar uchun kunlik hisobot:
```
📊 KUNLIK HISOBOT
📅 20.01.2026

👥 Jami qarzlar: 25 ta
💵 Umumiy: $3,450.00
💸 Umumiy: 44,850,000 so'm

📈 Bugun yangi: 3 ta
✅ Bugun to'landi: 5 ta
```

## 🔧 Muammolarni hal qilish

### Bot token xatosi
```
❌ Bot token topilmadi
```
**Yechim:** `.env` faylda `TELEGRAM_BOT_TOKEN` ni tekshiring

### Chat ID xatosi
```
⚠️ Mijoz uchun Telegram ID mavjud emas
```
**Yechim:** 
- Mijoz ma'lumotlarida `telegram_chat_id` ni kiriting
- Mijoz botga `/start` yuborishi kerak

### Xabar yuborilmadi
```
❌ Telegram xatosi: Forbidden: bot was blocked by the user
```
**Yechim:** Mijoz botni bloklagan, unblock qilishi kerak

### Scheduler ishga tushmadi
```
⚠️ Telegram bot scheduler ishga tushmadi
```
**Yechim:** 
- `pip install python-telegram-bot apscheduler`
- `.env` fayldagi token va chat ID larni tekshiring

## 📝 Fayllar tuzilishi

```
d:\hisobot\Jamshid\
│
├── telegram_bot.py              # Asosiy bot funksiyalari
├── debt_scheduler.py            # Avtomatik eslatmalar
├── telegram_config.py           # Sozlamalar va konstantalar
├── add_telegram_chat_id_migration.py  # Database migration
├── .env.telegram.example        # .env namuna
├── requirements.txt             # Dependencies (yangilangan)
├── app.py                       # Flask app (yangilangan)
└── TELEGRAM_BOT_SETUP.md        # Bu yo'riqnoma
```

## 🎉 Qo'shimcha imkoniyatlar

### Mijoz uchun bot commandlari

Bot'ga quyidagi commandlarni qo'shish mumkin:

- `/start` - Botni boshlash
- `/help` - Yordam
- `/mydebt` - Qarzimni ko'rish
- `/history` - To'lovlar tarixi
- `/contact` - Bog'lanish

### Admin panel

Admin uchun maxsus commandlar:

- `/stats` - Statistika
- `/debts` - Barcha qarzlar ro'yxati
- `/sendall` - Hammaga xabar yuborish
- `/export` - Excel/PDF export

### SMS va Telegram birgalikda

Loyihangizda allaqachon SMS xizmati (Eskiz.uz) bor. Ikkisini birgalikda ishlatish:

```python
# SMS va Telegram birgalikda yuborish
from sms_eskiz import EskizSMS

sms = EskizSMS()
scheduler = get_scheduler_instance(app, db)

# SMS yuborish
sms.send_debt_reminder(phone, customer_name, debt_usd, rate, location_name)

# Telegram yuborish
asyncio.run(
    scheduler.send_instant_reminder(
        customer_id, debt_usd, debt_uzs, location_name
    )
)
```

## ⚙️ Production deployment

Production muhitida ishga tushirish:

```bash
# Gunicorn bilan
gunicorn -c gunicorn_config.py app:app

# yoki systemd service sifatida
sudo systemctl start flask-app
```

Scheduler avtomatik ishga tushadi.

## 📞 Yordam va qo'llab-quvvatlash

Savollar yoki muammolar bo'lsa:
- 📧 Email: support@example.uz
- 📱 Telegram: @support_bot
- 📚 Dokumentatsiya: https://docs.example.uz

## 📜 Litsenziya

Loyihangizning litsenziyasiga mos.

---

✅ **Tayyor!** Endi sizning qarz tizimi Telegram orqali avtomatik xabarlar yuboradi!

🎯 **Keyingi qadamlar:**
1. Bot tokenini oling
2. .env faylni sozlang
3. Migration ni bajaring
4. App ni ishga tushiring
5. Test qiling!

Omad! 🚀
