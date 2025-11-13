import psutil

# ---------------- CPU Usage ----------------
def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)

# ---------------- Memory Usage ----------------
def get_memory_usage():
    return psutil.virtual_memory().percent

# ---------------- Disk Speed ----------------
last_read = psutil.disk_io_counters().read_bytes
last_write = psutil.disk_io_counters().write_bytes

def get_disk_speed():
    global last_read, last_write
    counters = psutil.disk_io_counters()

    read_speed = (counters.read_bytes - last_read) / 1024
    write_speed = (counters.write_bytes - last_write) / 1024

    last_read = counters.read_bytes
    last_write = counters.write_bytes

    return read_speed, write_speed

# ---------------- Network Speed ----------------
last_up = psutil.net_io_counters().bytes_sent
last_down = psutil.net_io_counters().bytes_recv

def get_network_speed():
    global last_up, last_down
    counters = psutil.net_io_counters()

    upload = (counters.bytes_sent - last_up) / 1024
    download = (counters.bytes_recv - last_down) / 1024

    last_up = counters.bytes_sent
    last_down = counters.bytes_recv

    return download, upload
