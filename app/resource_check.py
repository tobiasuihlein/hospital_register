import psutil
import os

def get_process_memory(process):
    try:
        return process.memory_info().rss / (1024 * 1024)  # in MB
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return 0

print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
print(f"Memory Usage: {psutil.virtual_memory().percent}%")

print("\nTop 5 CPU-consuming processes:")
processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)
for p in processes[-5:]:
    print(f"{p.info['name']} (PID: {p.info['pid']}): CPU {p.info['cpu_percent']}%, Memory {get_process_memory(p):.2f} MB")

print("\nTop 5 Memory-consuming processes:")
processes = sorted(psutil.process_iter(['pid', 'name']), key=get_process_memory, reverse=True)
for p in processes[:5]:
    print(f"{p.info['name']} (PID: {p.info['pid']}): Memory {get_process_memory(p):.2f} MB")