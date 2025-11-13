import psutil
import time

old_net = psutil.net_io_counters()
old_disk = psutil.disk_io_counters()
old_time = time.time()

def get_usage():
    global old_net, old_disk, old_time

    new_net = psutil.net_io_counters()
    new_disk = psutil.disk_io_counters()
    new_time = time.time()

    interval = new_time - old_time

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    read_speed = (new_disk.read_bytes - old_disk.read_bytes) / interval / 1024
    write_speed = (new_disk.write_bytes - old_disk.write_bytes) / interval / 1024

    upload = (new_net.bytes_sent - old_net.bytes_sent) / interval / 1024
    download = (new_net.bytes_recv - old_net.bytes_recv) / interval / 1024

    old_net = new_net
    old_disk = new_disk
    old_time = new_time

    return {
        "cpu": cpu,
        "mem": mem,
        "read": read_speed,
        "write": write_speed,
        "upload": upload,
        "download": download
    }
