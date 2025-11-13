import tkinter as tk
import psutil
import time

root = tk.Tk()
root.title("Real Time Process Monitoring Dashboard")
root.state("zoomed")
root.config(bg="#1e1e2e")

# ---------------- Card creator -----------------
def create_card(parent, title, color, row, col):
    card = tk.Frame(parent, bg=color, bd=3, relief="ridge")
    card.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")  # smaller padding

    title_lbl = tk.Label(card, text=title, bg=color, fg="white",
                         font=("Segoe UI", 16, "bold"))  # smaller title font
    title_lbl.pack(anchor="w", padx=10, pady=3)

    value_lbl = tk.Label(card, text="--", bg=color, fg="white",
                         font=("Segoe UI", 28, "bold"))  # smaller value font
    value_lbl.pack(anchor="w", padx=10, pady=6)

    return value_lbl


# Main grid container
grid_frame = tk.Frame(root, bg="#1e1e2e")
grid_frame.pack(fill="both", expand=True)

# Compact grid
grid_frame.grid_columnconfigure(0, weight=1)
grid_frame.grid_columnconfigure(1, weight=1)
grid_frame.grid_rowconfigure(0, weight=1)
grid_frame.grid_rowconfigure(1, weight=1)

# Create cards (compact color blocks)
cpu_lbl = create_card(grid_frame, "🔥 CPU Usage", "#ff4141", 0, 0)
mem_lbl = create_card(grid_frame, "📘 Memory Usage", "#43a2ff", 0, 1)
disk_lbl = create_card(grid_frame, "💾 Disk Speed", "#b043ff", 1, 0)
net_lbl = create_card(grid_frame, "🌐 Network Speed", "#39ff85", 1, 1)


# -------- Old values for speed calculations --------
old_net = psutil.net_io_counters()
old_disk = psutil.disk_io_counters()
old_time = time.time()


# ---------------- Update Function -----------------
def update_dashboard():
    global old_net, old_disk, old_time

    new_net = psutil.net_io_counters()
    new_disk = psutil.disk_io_counters()
    new_time = time.time()

    interval = new_time - old_time

    # Fast Data
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    cpu_lbl.config(text=f"{cpu}%")
    mem_lbl.config(text=f"{mem}%")

    # Disk Speed (KB/s)
    read_speed = (new_disk.read_bytes - old_disk.read_bytes) / interval / 1024
    write_speed = (new_disk.write_bytes - old_disk.write_bytes) / interval / 1024
    disk_lbl.config(text=f"{read_speed:.1f} KB/s | {write_speed:.1f} KB/s")

    # Network Speed (KB/s)
    upload = (new_net.bytes_sent - old_net.bytes_sent) / interval / 1024
    download = (new_net.bytes_recv - old_net.bytes_recv) / interval / 1024
    net_lbl.config(text=f"{upload:.1f} KB/s | {download:.1f} KB/s")

    old_net = new_net
    old_disk = new_disk
    old_time = new_time

    root.after(2000, update_dashboard)


# Title (smaller now)
tk.Label(root, text="⚙ Processes Status Dashboard",
         fg="white", bg="#1e1e2e",
         font=("Segoe UI", 26, "bold")
         ).pack(pady=10)

update_dashboard()
root.mainloop()
