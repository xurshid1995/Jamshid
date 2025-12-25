#!/bin/bash
# 165.232.81.142 serverga deployment qilish

echo "🚀 Starting deployment to 165.232.81.142..."
echo ""

# 1. Serverga SSH orqali ulanish va fayllarni yangilash
echo "📥 Step 1: Pulling latest code from GitHub..."
ssh root@165.232.81.142 << 'ENDSSH'
cd /var/www/dokon
git pull origin main
ENDSSH

echo ""

# 2. PostgreSQL timeout sozlamalarini o'rnatish
echo "🗄️  Step 2: Setting PostgreSQL timeouts..."
ssh root@165.232.81.142 << 'ENDSSH'
cd /var/www/dokon
psql -U postgres -d dokon_db -f set_pg_timeouts.sql
ENDSSH

echo ""

# 3. Nginx konfiguratsiyasini yangilash
echo "🔧 Step 3: Updating Nginx configuration..."
ssh root@165.232.81.142 << 'ENDSSH'
# Backup old config
cp /etc/nginx/sites-available/dokon /etc/nginx/sites-available/dokon.backup.$(date +%Y%m%d_%H%M%S)

# Copy new config
cp /var/www/dokon/nginx_dokon.conf /etc/nginx/sites-available/dokon

# Test nginx configuration
nginx -t

# Reload nginx if test passes
if [ $? -eq 0 ]; then
    systemctl reload nginx
    echo "✅ Nginx reloaded successfully"
else
    echo "❌ Nginx configuration test failed!"
    exit 1
fi
ENDSSH

echo ""

# 4. Gunicorn servisini qayta ishga tushirish
echo "🔄 Step 4: Restarting Gunicorn service..."
ssh root@165.232.81.142 << 'ENDSSH'
# Stop service
systemctl stop dokon

# Wait 2 seconds
sleep 2

# Start service
systemctl start dokon

# Check status
systemctl status dokon --no-pager

# Check if service is active
if systemctl is-active --quiet dokon; then
    echo "✅ Gunicorn service is running"
else
    echo "❌ Gunicorn service failed to start!"
    journalctl -u dokon -n 50 --no-pager
    exit 1
fi
ENDSSH

echo ""

# 5. Deployment natijalarini tekshirish
echo "🔍 Step 5: Checking deployment results..."
ssh root@165.232.81.142 << 'ENDSSH'
echo "📊 Service Status:"
systemctl status dokon --no-pager -l | head -n 15

echo ""
echo "📝 Recent Logs:"
tail -n 20 /var/www/dokon/logs/error.log

echo ""
echo "🌐 Nginx Status:"
systemctl status nginx --no-pager | head -n 5
ENDSSH

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🔗 Test the application:"
echo "   http://165.232.81.142"
echo ""
echo "📊 Monitor logs:"
echo "   ssh root@165.232.81.142 'tail -f /var/www/dokon/logs/error.log'"
echo ""
