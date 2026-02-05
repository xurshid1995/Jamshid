# Server loglarini real-time kuzatish
# Foydalanish: .\monitor_logs.ps1

$SERVER = "139.59.154.185"

Write-Host "🔍 Server monitoring boshlandi: $SERVER" -ForegroundColor Green
Write-Host "Ctrl+C bosing to'xtatish uchun" -ForegroundColor Yellow
Write-Host "=" * 80

# Real-time log monitoring
ssh root@$SERVER "journalctl -u jamshid-app -f | grep --line-buffered -E '(ERROR|Exception|XATOLIK|⚠️|❌)'"
