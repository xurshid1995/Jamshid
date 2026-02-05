# Server holatini tekshirish
# Foydalanish: .\check_server.ps1

$SERVER = "139.59.154.185"

Write-Host "`n🔍 SERVER DIAGNOSTICS: $SERVER" -ForegroundColor Cyan
Write-Host "=" * 80

# 1. Server online/offline
Write-Host "`n1️⃣  Server Ping Test:" -ForegroundColor Yellow
Test-Connection -ComputerName $SERVER -Count 2 -Quiet
if ($?) {
    Write-Host "   ✅ Server online" -ForegroundColor Green
} else {
    Write-Host "   ❌ Server offline!" -ForegroundColor Red
    exit 1
}

# 2. Flask application status
Write-Host "`n2️⃣  Flask Application Status:" -ForegroundColor Yellow
ssh root@$SERVER "systemctl is-active jamshid-app"
if ($?) {
    Write-Host "   ✅ Application running" -ForegroundColor Green
} else {
    Write-Host "   ❌ Application stopped!" -ForegroundColor Red
}

# 3. PostgreSQL status
Write-Host "`n3️⃣  PostgreSQL Status:" -ForegroundColor Yellow
ssh root@$SERVER "systemctl is-active postgresql"
if ($?) {
    Write-Host "   ✅ Database running" -ForegroundColor Green
} else {
    Write-Host "   ❌ Database stopped!" -ForegroundColor Red
}

# 4. Nginx status
Write-Host "`n4️⃣  Nginx Status:" -ForegroundColor Yellow
ssh root@$SERVER "systemctl is-active nginx"
if ($?) {
    Write-Host "   ✅ Nginx running" -ForegroundColor Green
} else {
    Write-Host "   ❌ Nginx stopped!" -ForegroundColor Red
}

# 5. CPU & Memory usage
Write-Host "`n5️⃣  System Resources:" -ForegroundColor Yellow
ssh root@$SERVER "top -bn1 | head -5"

# 6. Disk usage
Write-Host "`n6️⃣  Disk Usage:" -ForegroundColor Yellow
ssh root@$SERVER "df -h | grep -E '^/dev/|Filesystem'"

# 7. Recent errors (last 10)
Write-Host "`n7️⃣  Recent Errors (last 10):" -ForegroundColor Yellow
ssh root@$SERVER "journalctl -u jamshid-app --since='30 minutes ago' | grep -i error | tail -10"

# 8. Active connections
Write-Host "`n8️⃣  Database Connections:" -ForegroundColor Yellow
ssh root@$SERVER "sudo -u postgres psql -d sayt_db -t -c 'SELECT COUNT(*) FROM pg_stat_activity WHERE datname=''sayt_db'';'"

# 9. Today's sales count
Write-Host "`n9️⃣  Today's Sales:" -ForegroundColor Yellow
ssh root@$SERVER "sudo -u postgres psql -d sayt_db -t -c 'SELECT COUNT(*) FROM sales WHERE DATE(sale_date) = CURRENT_DATE;'"

Write-Host "`n" + "=" * 80
Write-Host "✅ Diagnostics completed!" -ForegroundColor Green
