import psutil

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def get_cpu_percore():
    return psutil.cpu_percent(interval=0.1, percpu=True)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used / (1024**3), mem.total / (1024**3)

last_read = psutil.disk_io_counters().read_bytes
last_write = psutil.disk_io_counters().write_bytes

def get_disk_speed():
    global last_read, last_write
    io = psutil.disk_io_counters()
    read = (io.read_bytes - last_read) / 1024
    write = (io.write_bytes - last_write) / 1024
    last_read = io.read_bytes
    last_write = io.write_bytes
    return read, write

last_up = psutil.net_io_counters().bytes_sent
last_down = psutil.net_io_counters().bytes_recv

def get_network_speed():
    global last_up, last_down
    io = psutil.net_io_counters()
    upload = (io.bytes_sent - last_up) / 1024
    download = (io.bytes_recv - last_down) / 1024
    last_up = io.bytes_sent
    last_down = io.bytes_recv
    return download, upload

# GPU
try:
    from pynvml import (
        nvmlInit,
        nvmlDeviceGetHandleByIndex,
        nvmlDeviceGetUtilizationRates,
        nvmlDeviceGetMemoryInfo
    )
    gpu_available = True
except:
    gpu_available = False

def get_gpu_usage():
    if not gpu_available:
        return None

    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        util = nvmlDeviceGetUtilizationRates(handle)
        gpu = util.gpu

        mem = nvmlDeviceGetMemoryInfo(handle)
        used = mem.used / (1024**2)
        total = mem.total / (1024**2)

        return gpu, used, total
    except:
        return None
