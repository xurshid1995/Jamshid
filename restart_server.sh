#!/bin/bash
# Server restart script
# Run this on the production server via SSH

echo "🔄 Restarting server..."

# Stop the service
sudo systemctl stop sayt2025

# Wait a moment
sleep 2

# Start the service
sudo systemctl start sayt2025

# Check status
sudo systemctl status sayt2025

echo "✅ Server restarted!"
echo ""
echo "📊 Check logs with:"
echo "   sudo journalctl -u sayt2025 -n 50 -f"
