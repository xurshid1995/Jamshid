# -*- coding: utf-8 -*-
"""
Server Monitoring Script
Real-time server monitoring va Telegram orqali ogohlantirish
"""
import os
import sys
import time
import logging
import requests
import psutil
from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from telegram import Bot
from sqlalchemy import create_engine, text
import urllib.parse

# Environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServerMonitor:
    """Server monitoring class"""
    
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.admin_chat_ids = self._parse_admin_ids()
        self.bot = None
        self.db_engine = None
        
        # Alert thresholds
        self.cpu_threshold = 80  # CPU > 80%
        self.memory_threshold = 85  # Memory > 85%
        self.disk_threshold = 90  # Disk > 90%
        self.check_interval = 300  # 5 daqiqa
        
        # Initialize Telegram
        if self.telegram_token:
            try:
                self.bot = Bot(token=self.telegram_token)
                logger.info("✅ Telegram bot initialized")
            except Exception as e:
                logger.error(f"❌ Telegram bot error: {e}")
        
        # Initialize Database
        self._init_database()
    
    def _parse_admin_ids(self):
        """Parse admin chat IDs from environment"""
        admin_ids_str = os.getenv('TELEGRAM_ADMIN_CHAT_IDS', '')
        if not admin_ids_str:
            return []
        return [int(id_.strip()) for id_ in admin_ids_str.split(',') if id_.strip()]
    
    def _init_database(self):
        """Initialize database connection"""
        try:
            db_params = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB_NAME', 'sayt_db'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'postgres')
            }
            
            safe_password = urllib.parse.quote_plus(db_params['password'])
            database_url = f"postgresql://{db_params['user']}:{safe_password}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
            
            self.db_engine = create_engine(database_url, pool_pre_ping=True)
            logger.info("✅ Database connection initialized")
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
    
    async def send_alert(self, message):
        """Send alert to Telegram admins"""
        if not self.bot or not self.admin_chat_ids:
            logger.warning("⚠️ Telegram bot yoki admin IDs sozlanmagan")
            return
        
        for chat_id in self.admin_chat_ids:
            try:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=f"🚨 *SERVER ALERT*\n\n{message}",
                    parse_mode='Markdown'
                )
                logger.info(f"✅ Alert sent to {chat_id}")
            except Exception as e:
                logger.error(f"❌ Failed to send alert to {chat_id}: {e}")
    
    def check_system_resources(self):
        """Check CPU, Memory, Disk usage"""
        alerts = []
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.cpu_threshold:
            alerts.append(f"⚠️ CPU usage: {cpu_percent}% (threshold: {self.cpu_threshold}%)")
        
        # Memory usage
        memory = psutil.virtual_memory()
        if memory.percent > self.memory_threshold:
            alerts.append(f"⚠️ Memory usage: {memory.percent}% (threshold: {self.memory_threshold}%)")
        
        # Disk usage
        disk = psutil.disk_usage('/')
        if disk.percent > self.disk_threshold:
            alerts.append(f"⚠️ Disk usage: {disk.percent}% (threshold: {self.disk_threshold}%)")
        
        return alerts
    
    def check_database(self):
        """Check database status"""
        if not self.db_engine:
            return ["❌ Database connection not initialized"]
        
        alerts = []
        try:
            with self.db_engine.connect() as conn:
                # Check active connections
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM pg_stat_activity WHERE datname = :db_name"
                ), {"db_name": os.getenv('DB_NAME', 'sayt_db')})
                active_connections = result.scalar()
                
                if active_connections > 50:  # Warning if > 50 connections
                    alerts.append(f"⚠️ Database connections: {active_connections} (high)")
                
                # Check today's sales
                result = conn.execute(text(
                    "SELECT COUNT(*) FROM sales WHERE DATE(sale_date) = CURRENT_DATE"
                ))
                today_sales = result.scalar()
                logger.info(f"📊 Today's sales: {today_sales}")
                
        except Exception as e:
            alerts.append(f"❌ Database check failed: {str(e)}")
        
        return alerts
    
    def check_application(self):
        """Check Flask application status"""
        alerts = []
        
        # Try to ping the application
        try:
            response = requests.get(
                "http://localhost:8000/health",  # Health check endpoint
                timeout=5
            )
            if response.status_code != 200:
                alerts.append(f"⚠️ Application returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            alerts.append(f"❌ Application not responding: {str(e)}")
        
        return alerts
    
    def get_status_report(self):
        """Generate full status report"""
        report_lines = [
            f"📊 *Server Status Report*",
            f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "*System Resources:*"
        ]
        
        # System resources
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        report_lines.extend([
            f"  CPU: {cpu}%",
            f"  Memory: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)",
            f"  Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)",
            ""
        ])
        
        # Database status
        if self.db_engine:
            try:
                with self.db_engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM sales WHERE DATE(sale_date) = CURRENT_DATE"))
                    today_sales = result.scalar()
                    report_lines.append(f"*Database:*")
                    report_lines.append(f"  ✅ Connected")
                    report_lines.append(f"  📈 Today's sales: {today_sales}")
                    report_lines.append("")
            except Exception as e:
                report_lines.append(f"*Database:*")
                report_lines.append(f"  ❌ Error: {str(e)}")
                report_lines.append("")
        
        return "\n".join(report_lines)
    
    async def run_monitoring(self):
        """Main monitoring loop"""
        logger.info("🔍 Server monitoring started")
        
        # Send initial status
        try:
            status = self.get_status_report()
            await self.send_alert(f"✅ Monitoring started\n\n{status}")
        except Exception as e:
            logger.error(f"Failed to send initial status: {e}")
        
        while True:
            try:
                all_alerts = []
                
                # Check system resources
                all_alerts.extend(self.check_system_resources())
                
                # Check database
                all_alerts.extend(self.check_database())
                
                # Check application
                all_alerts.extend(self.check_application())
                
                # Send alerts if any
                if all_alerts:
                    alert_message = "\n".join(all_alerts)
                    await self.send_alert(alert_message)
                    logger.warning(f"Alerts sent: {len(all_alerts)}")
                else:
                    logger.info("✅ All systems normal")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("⏹️ Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute on error

if __name__ == "__main__":
    import asyncio
    
    monitor = ServerMonitor()
    
    # Run monitoring
    try:
        asyncio.run(monitor.run_monitoring())
    except KeyboardInterrupt:
        logger.info("👋 Monitoring stopped")
