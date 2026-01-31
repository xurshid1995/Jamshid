"""Gunicorn configuration file"""
import multiprocessing
import os

# Server socket - faqat localhost (xavfsizlik uchun)
bind = os.getenv('BIND', '127.0.0.1:8000')
backlog = 2048

# Worker processes - 2 CPU uchun optimal: 3 worker
# Formula: (2 * CPU_count) - 1 yoki 3 (xotira tejash uchun)
workers = int(os.getenv('WORKERS', 3))  # 2 CPU uchun 3 worker optimal
worker_class = 'sync'
worker_connections = 1000
timeout = int(os.getenv('TIMEOUT', 120))  # 2 minut - oddiy requestlar uchun yetarli
keepalive = 2  # Keep-alive connection 2 sekund

# Request size limits (100MB - rasmlar uchun)
limit_request_line = 8190  # Request line length
limit_request_fields = 200  # Request header count
limit_request_field_size = 0  # No limit on header size (default 8190)

# Logging
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'sayt_2025'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
