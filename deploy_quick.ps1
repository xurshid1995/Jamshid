# Tezkor Deploy Script - Jamshid Server
# Foydalanish: .\deploy_quick.ps1

Write-Host "🚀 Jamshid serverga deploy boshlanmoqda..." -ForegroundColor Cyan
Write-Host ""

# Server'ga SSH orqali ulanish va deploy
$deployCommands = "cd /var/www/jamshid && git pull origin main && systemctl restart jamshid && systemctl status jamshid --no-pager | head -15"

ssh root@139.59.154.185 $deployCommands

Write-Host ""
Write-Host "✅ Deploy yakunlandi!" -ForegroundColor Green
Write-Host "🌐 Server: http://139.59.154.185" -ForegroundColor Yellow
