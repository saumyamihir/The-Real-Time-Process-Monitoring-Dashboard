import tkinter as tk
from ui import create_card
from utils import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_speed,
    get_network_speed
)

root = tk.Tk()
root.title("Real Time Process Monitoring Dashboard")
root.state("zoomed")
root.config(bg="#1e1e2e")

# Grid expand
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# ---------------- Create Cards -----------------
cpu_label = create_card(root, "🔥 CPU Usage", "#ff3b30", 0, 0)
memory_label = create_card(root, "🧩 Memory Usage", "#1e90ff", 0, 1)
disk_label = create_card(root, "💾 Disk Speed", "#a64ff5", 1, 0)
net_label = create_card(root, "🌐 Network Speed", "#22d66f", 1, 1)

# ---------------- Update Loop -----------------
def update_dashboard():
    cpu_label.config(text=f"{get_cpu_usage()}%")
    memory_label.config(text=f"{get_memory_usage()}%")

    read, write = get_disk_speed()
    disk_label.config(text=f"{read:.1f} KB/s | {write:.1f} KB/s")

    download, upload = get_network_speed()
    net_label.config(text=f"{download:.1f} KB/s | {upload:.1f} KB/s")

    root.after(1000, update_dashboard)

update_dashboard()
root.mainloop()
