import tkinter as tk
from ui import create_sidebar_button, create_graph_frame
from utils import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_speed,
    get_network_speed
)

root = tk.Tk()
root.title("System Monitor")
root.geometry("1000x650")
root.config(bg="#1e1e2e")

# ================= Sidebar =================
sidebar = tk.Frame(root, bg="#111", width=180)
sidebar.pack(side="left", fill="y")

content = tk.Frame(root, bg="#1e1e2e")
content.pack(side="right", fill="both", expand=True)

current_frame = None

def show_frame(frame):
    global current_frame
    if current_frame is not None:
        current_frame.pack_forget()
    current_frame = frame
    current_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------- CPU Page ----------------
cpu_frame, cpu_ax, cpu_line, cpu_canvas = create_graph_frame(content, "CPU Usage")
cpu_data = []

def update_cpu():
    cpu = get_cpu_usage()
    cpu_data.append(cpu)
    cpu_data[:] = cpu_data[-50:]
    cpu_line.set_data(range(len(cpu_data)), cpu_data)

    cpu_ax.set_xlim(0, 50)
    cpu_ax.set_ylim(0, 100)
    cpu_canvas.draw()

    if current_frame == cpu_frame:
        root.after(800, update_cpu)

# ---------------- Memory Page ----------------
mem_frame, mem_ax, mem_line, mem_canvas = create_graph_frame(content, "Memory Usage")
mem_data = []

def update_memory():
    mem = get_memory_usage()
    mem_data.append(mem)
    mem_data[:] = mem_data[-50:]
    mem_line.set_data(range(len(mem_data)), mem_data)

    mem_ax.set_xlim(0, 50)
    mem_ax.set_ylim(0, 100)
    mem_canvas.draw()

    if current_frame == mem_frame:
        root.after(800, update_memory)

# ---------------- Disk Page ----------------
disk_frame, disk_ax, disk_line, disk_canvas = create_graph_frame(content, "Disk Speed")
disk_data = []

def update_disk():
    r, w = get_disk_speed()
    disk_data.append(r + w)
    disk_data[:] = disk_data[-50:]
    disk_line.set_data(range(len(disk_data)), disk_data)

    disk_ax.set_xlim(0, 50)
    disk_ax.set_ylim(0, max(50, max(disk_data)))
    disk_canvas.draw()

    if current_frame == disk_frame:
        root.after(800, update_disk)

# ---------------- Network Page ----------------
net_frame, net_ax, net_line, net_canvas = create_graph_frame(content, "Network Speed")
net_data = []

def update_network():
    d, u = get_network_speed()
    net_data.append(d + u)
    net_data[:] = net_data[-50:]
    net_line.set_data(range(len(net_data)), net_data)

    net_ax.set_xlim(0, 50)
    net_ax.set_ylim(0, max(50, max(net_data)))
    net_canvas.draw()

    if current_frame == net_frame:
        root.after(800, update_network)

# ================= Sidebar Buttons =================
create_sidebar_button(sidebar, "CPU Usage", lambda: [show_frame(cpu_frame), update_cpu()]).pack(fill="x", pady=5)
create_sidebar_button(sidebar, "Memory Usage", lambda: [show_frame(mem_frame), update_memory()]).pack(fill="x", pady=5)
create_sidebar_button(sidebar, "Disk Speed", lambda: [show_frame(disk_frame), update_disk()]).pack(fill="x", pady=5)
create_sidebar_button(sidebar, "Network", lambda: [show_frame(net_frame), update_network()]).pack(fill="x", pady=5)

root.mainloop()
