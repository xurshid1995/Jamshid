#!/bin/bash
# Manual deploy script - Serverda bajarish uchun
# SSH: ssh jamshid@139.59.154.185
# Parol: Teleport7799

echo "🚀 Starting deployment..."

# 1. Loyiha papkasiga o'tish
cd /var/www/jamshid || { echo "❌ Papka topilmadi"; exit 1; }

echo "📂 Current directory: $(pwd)"

# 2. Git status
echo "📊 Checking git status..."
git status

# 3. Yangi kodlarni olish
echo "⬇️ Pulling latest code from origin/main..."
git pull origin main

# 4. Dependencies yangilash (agar kerak bo'lsa)
# source venv/bin/activate
# pip install -r requirements.txt

# 5. Gunicorn'ni qayta ishga tushirish
echo "🔄 Restarting gunicorn service..."
sudo systemctl restart jamshid

# 6. Service statusini tekshirish
echo "✅ Checking service status..."
sudo systemctl status jamshid --no-pager

# 7. Nginx reload (agar kerak bo'lsa)
# sudo systemctl reload nginx

echo ""
echo "✅ Deployment completed!"
echo "🌐 Check your website: http://139.59.154.185/products"
