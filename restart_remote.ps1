# Remote server restart script
# Usage: .\restart_remote.ps1

$server = "139.59.154.185"
$user = "root"
$password = "Teleport7799"
$service = "jamshid"

Write-Host "Connecting to server..." -ForegroundColor Yellow

# SSH command to restart server
$commands = "systemctl restart $service && echo 'Service restarted' && systemctl status $service --no-pager -l"

# Using plink (PuTTY command line) if available
if (Get-Command plink -ErrorAction SilentlyContinue) {
    echo y | plink -pw $password $user@$server $commands
} else {
    Write-Host "plink not found. Using SSH (you may need to enter password manually)" -ForegroundColor Cyan
    Write-Host "Password: $password" -ForegroundColor Green
    Write-Host ""
    
    # This will prompt for password
    ssh "$user@$server" $commands
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
