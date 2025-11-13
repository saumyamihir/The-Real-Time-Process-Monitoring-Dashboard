import tkinter as tk
from ui import create_card, create_graph
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

# ---------------- Grid Setup ----------------
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=2)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# ---------------- Create Cards -----------------
cpu_card, cpu_label = create_card(root, "🔥 CPU Usage", "#ff3b30", 0, 0)
memory_card, memory_label = create_card(root, "🧩 Memory Usage", "#1e90ff", 0, 1)
disk_card, disk_label = create_card(root, "💾 Disk Speed", "#a64ff5", 1, 0)
net_card, net_label = create_card(root, "🌐 Network Speed", "#22d66f", 1, 1)

# ---------------- Graph Container -----------------
graph_container = tk.Frame(root, bg="#1e1e2e")
graph_container.grid(row=2, column=0, columnspan=2, sticky="nsew")

# ---------------- Graphs -----------------
cpu_ax, cpu_line, cpu_canvas = create_graph(graph_container, "CPU Usage Graph")
mem_ax, mem_line, mem_canvas = create_graph(graph_container, "Memory Usage Graph")
disk_ax, disk_line, disk_canvas = create_graph(graph_container, "Disk Speed Graph")
net_ax, net_line, net_canvas = create_graph(graph_container, "Network Speed Graph")

cpu_data, mem_data, disk_data, net_data = [], [], [], []

# ---------------- Update Loop -----------------
def update_dashboard():
    # CPU update
    cpu = get_cpu_usage()
    cpu_label.config(text=f"{cpu}%")
    cpu_data.append(cpu)
    cpu_data[:] = cpu_data[-50:]
    cpu_line.set_data(range(len(cpu_data)), cpu_data)
    cpu_ax.set_xlim(0, 50)
    cpu_ax.set_ylim(0, 100)
    cpu_canvas.draw()

    # Memory update
    memory = get_memory_usage()
    memory_label.config(text=f"{memory}%")
    mem_data.append(memory)
    mem_data[:] = mem_data[-50:]
    mem_line.set_data(range(len(mem_data)), mem_data)
    mem_ax.set_xlim(0, 50)
    mem_ax.set_ylim(0, 100)
    mem_canvas.draw()

    # Disk update
    read, write = get_disk_speed()
    disk_label.config(text=f"{read:.1f} KB/s | {write:.1f} KB/s")
    disk_data.append(read + write)
    disk_data[:] = disk_data[-50:]
    disk_line.set_data(range(len(disk_data)), disk_data)
    disk_ax.set_xlim(0, 50)
    disk_ax.set_ylim(0, max(50, max(disk_data)))
    disk_canvas.draw()

    # Network update
    download, upload = get_network_speed()
    net_label.config(text=f"{download:.1f} KB/s | {upload:.1f} KB/s")
    net_data.append(download + upload)
    net_data[:] = net_data[-50:]
    net_line.set_data(range(len(net_data)), net_data)
    net_ax.set_xlim(0, 50)
    net_ax.set_ylim(0, max(50, max(net_data)))
    net_canvas.draw()

    root.after(1000, update_dashboard)

update_dashboard()
root.mainloop()
