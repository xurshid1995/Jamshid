# Server Monitoring Guide

Server holatini kuzatish va monitoring qilish uchun qo'llanma.

## 1. Tezkor Tekshirish (Quick Check)

### Windows PowerShell orqali:
```powershell
# Server holatini tekshirish
.\check_server.ps1
```

Bu script quyidagilarni tekshiradi:
- ✅ Server online/offline
- ✅ Flask application holati
- ✅ PostgreSQL database holati
- ✅ Nginx holati
- ✅ CPU & Memory
- ✅ Disk usage
- ✅ Oxirgi xatolar
- ✅ Bugungi sotuvlar

## 2. Real-time Log Monitoring

### Faqat xatolarni ko'rish:
```powershell
.\monitor_logs.ps1
```

### Barcha loglarni ko'rish:
```powershell
ssh root@139.59.154.185 "journalctl -u jamshid-app -f"
```

### Oxirgi 100 ta log:
```powershell
ssh root@139.59.154.185 "journalctl -u jamshid-app -n 100 --no-pager"
```

## 3. Python Monitoring Script (Avtomatik)

### Lokal kompyuterda ishlatish:
```bash
# Python virtual environment
.\.venv\Scripts\Activate.ps1

# Monitoring script ishga tushirish
python server_monitor.py
```

Bu script:
- 🔍 Har 5 daqiqada server holatini tekshiradi
- 📊 CPU, Memory, Disk usage'ni monitor qiladi
- 💾 Database connection'ni tekshiradi
- 📱 Muammo bo'lganda Telegram orqali ogohlantiradi

### Serverda ishlatish (tavsiya qilinadi):
```bash
# Serverga ulanish
ssh root@139.59.154.185

# Script yuklab olish
cd /root
nano server_monitor.py
# (yuqoridagi server_monitor.py kodini joylashtiring)

# Background'da ishga tushirish
nohup python3 server_monitor.py > monitor.log 2>&1 &

# Loglarni ko'rish
tail -f monitor.log
```

## 4. Telegram Bot Monitoring

### .env faylini sozlash:
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_CHAT_IDS=123456789,987654321
```

### Telegram bot komandalar:
- `/status` - Server holati
- `/sales` - Bugungi sotuvlar
- `/errors` - Oxirgi xatolar

## 5. Web Health Check

### Browser yoki curl orqali:
```bash
# Public health check
curl http://139.59.154.185/health

# Response:
{
  "status": "healthy",
  "timestamp": "2026-02-05T16:30:00+05:00",
  "database": "connected",
  "stats": {
    "total_products": 5432,
    "today_sales": 47
  }
}
```

## 6. Database Monitoring

### PostgreSQL connection:
```bash
ssh root@139.59.154.185
sudo -u postgres psql sayt_db
```

### Foydali SQL querylar:

```sql
-- Active connections
SELECT COUNT(*) FROM pg_stat_activity WHERE datname='sayt_db';

-- Bugungi sotuvlar
SELECT COUNT(*), SUM(total_amount_uzs) 
FROM sales 
WHERE DATE(sale_date) = CURRENT_DATE;

-- Oxirgi 10 ta savdo
SELECT id, sale_date, total_amount_uzs, payment_status 
FROM sales 
ORDER BY sale_date DESC 
LIMIT 10;

-- Eng ko'p sotiladigan mahsulotlar (bugun)
SELECT p.name, SUM(si.quantity) as total_sold
FROM sale_items si
JOIN products p ON si.product_id = p.id
JOIN sales s ON si.sale_id = s.id
WHERE DATE(s.sale_date) = CURRENT_DATE
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;

-- Stock muammolari (0 yoki manfiy)
SELECT name, stock_quantity 
FROM products 
WHERE stock_quantity <= 0
ORDER BY name;
```

## 7. System Service Management

### Flask application:
```bash
# Status
sudo systemctl status jamshid-app

# Restart
sudo systemctl restart jamshid-app

# Logs
sudo journalctl -u jamshid-app -n 100
```

### PostgreSQL:
```bash
sudo systemctl status postgresql
sudo systemctl restart postgresql
```

### Nginx:
```bash
sudo systemctl status nginx
sudo systemctl restart nginx
sudo nginx -t  # Config test
```

## 8. Grafana/Prometheus (Advanced)

Kelajakda professional monitoring uchun:
- Grafana dashboard
- Prometheus metrics
- AlertManager notifications

## Troubleshooting

### Agar ilova ishlamasa:
```bash
# 1. Service holatini tekshirish
sudo systemctl status jamshid-app

# 2. Loglarni tekshirish
sudo journalctl -u jamshid-app -n 200

# 3. Restart
sudo systemctl restart jamshid-app

# 4. Gunicorn process
ps aux | grep gunicorn

# 5. Port tekshirish
sudo netstat -tlnp | grep 8000
```

### Database muammosi:
```bash
# PostgreSQL status
sudo systemctl status postgresql

# Connection test
sudo -u postgres psql -c "SELECT version();"

# Restart
sudo systemctl restart postgresql
```

### Xotira muammosi:
```bash
# Memory usage
free -h

# Top processes
top -o %MEM

# Kill process (agar kerak bo'lsa)
sudo pkill -9 gunicorn
sudo systemctl restart jamshid-app
```

## Avtomatik Monitoring Setup (Systemd Service)

### monitoring.service yaratish:
```bash
sudo nano /etc/systemd/system/monitoring.service
```

```ini
[Unit]
Description=Server Monitoring Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root
ExecStart=/usr/bin/python3 /root/server_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Enable va start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable monitoring.service
sudo systemctl start monitoring.service
sudo systemctl status monitoring.service
```

## Alert Thresholds

Script'dagi ogohlantirishlar:
- CPU > 80%
- Memory > 85%
- Disk > 90%
- Database connections > 50

Bu qiymatlarni `server_monitor.py` faylida o'zgartirish mumkin.
