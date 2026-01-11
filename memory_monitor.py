#!/usr/bin/env python3
"""
Xotira monitoring vositasi - Flask ilovaning xotira ishlatishini kuzatish
"""
import psutil
import time
import os
from datetime import datetime

def format_bytes(bytes):
    """Baytlarni MB/GB formatda ko'rsatish"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def monitor_process(pid=None, duration=60):
    """
    Jarayonni monitoring qilish
    
    Args:
        pid: Process ID (agar None bo'lsa, python jarayonlarni topadi)
        duration: Monitoring davomiyligi (sekund)
    """
    if pid is None:
        # Barcha Python jarayonlarni topish
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and 'app.py' in ' '.join(cmdline):
                        python_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if not python_processes:
            print("❌ Python jarayoni topilmadi!")
            return
        
        print(f"✅ {len(python_processes)} ta Python jarayon topildi\n")
        for proc in python_processes:
            pid = proc.pid
            monitor_single_process(pid, duration)
    else:
        monitor_single_process(pid, duration)

def monitor_single_process(pid, duration):
    """Bitta jarayonni monitoring qilish"""
    try:
        process = psutil.Process(pid)
        print(f"{'='*60}")
        print(f"PID: {pid}")
        print(f"Jarayon: {process.name()}")
        print(f"Start vaqti: {datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        start_time = time.time()
        max_memory = 0
        measurements = []
        
        while time.time() - start_time < duration:
            try:
                # Xotira ma'lumotlari
                mem_info = process.memory_info()
                mem_percent = process.memory_percent()
                
                # CPU ma'lumotlari
                cpu_percent = process.cpu_percent(interval=1)
                
                # Thread va connection sonlari
                num_threads = process.num_threads()
                try:
                    num_connections = len(process.connections())
                except psutil.AccessDenied:
                    num_connections = "N/A"
                
                current_memory = mem_info.rss
                if current_memory > max_memory:
                    max_memory = current_memory
                
                measurements.append({
                    'time': datetime.now(),
                    'memory': current_memory,
                    'cpu': cpu_percent
                })
                
                # Real-time ko'rsatish
                print(f"⏰ {datetime.now().strftime('%H:%M:%S')} | "
                      f"💾 RAM: {format_bytes(current_memory)} ({mem_percent:.1f}%) | "
                      f"🔥 CPU: {cpu_percent:.1f}% | "
                      f"🧵 Threads: {num_threads} | "
                      f"🔌 Connections: {num_connections}")
                
                time.sleep(2)  # Har 2 sekundda o'lchash
                
            except psutil.NoSuchProcess:
                print("\n❌ Jarayon to'xtatildi!")
                break
        
        # Statistika
        if measurements:
            avg_memory = sum(m['memory'] for m in measurements) / len(measurements)
            avg_cpu = sum(m['cpu'] for m in measurements) / len(measurements)
            
            print(f"\n{'='*60}")
            print("📊 STATISTIKA:")
            print(f"{'='*60}")
            print(f"⏱️  Monitoring vaqti: {duration} sekund")
            print(f"📈 O'rtacha RAM: {format_bytes(avg_memory)}")
            print(f"🔝 Maksimal RAM: {format_bytes(max_memory)}")
            print(f"💻 O'rtacha CPU: {avg_cpu:.1f}%")
            print(f"📊 O'lchovlar soni: {len(measurements)}")
            
            # Xotira o'sishi
            if len(measurements) > 1:
                memory_growth = measurements[-1]['memory'] - measurements[0]['memory']
                if memory_growth > 0:
                    print(f"⚠️  Xotira o'sishi: +{format_bytes(memory_growth)}")
                else:
                    print(f"✅ Xotira o'sishi: {format_bytes(memory_growth)}")
            
            print(f"{'='*60}\n")
            
    except psutil.NoSuchProcess:
        print(f"❌ PID {pid} topilmadi!")
    except psutil.AccessDenied:
        print(f"❌ PID {pid}ga kirish rad etildi! Administrator sifatida ishga tushiring.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask ilovaning xotira monitoring')
    parser.add_argument('--pid', type=int, help='Process ID')
    parser.add_argument('--duration', type=int, default=60, help='Monitoring davomiyligi (sekund)')
    
    args = parser.parse_args()
    
    print(f"\n🔍 Xotira Monitoring Boshlandi...")
    print(f"⏰ Davomiyligi: {args.duration} sekund\n")
    
    try:
        monitor_process(args.pid, args.duration)
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring to'xtatildi!")
