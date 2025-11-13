import tkinter as tk
import psutil
from ui import (
    create_topbar,
    create_sidebar_button,
    activate_button,
    create_graph_frame,
    create_pie_frame
)
from utils import (
    get_cpu_usage,
    get_cpu_percore,
    get_memory_usage,
    get_disk_speed,
    get_network_speed,
    get_gpu_usage
)

root = tk.Tk()
root.title("System Monitor Pro")
root.geometry("1100x700")
root.config(bg="#1e1e2e")

create_topbar(root, "🔥 System Monitor — Pro Edition")

# Main layout
layout = tk.Frame(root, bg="#1e1e2e")
layout.pack(fill="both", expand=True)

sidebar = tk.Frame(layout, bg="#111", width=200)
sidebar.pack(side="left", fill="y")

content = tk.Frame(layout, bg="#1e1e2e")
content.pack(side="right", fill="both", expand=True)

current_frame = None
buttons = []

def show_frame(frame):
    global current_frame
    if current_frame:
        current_frame.pack_forget()
    current_frame = frame
    current_frame.pack(fill="both", expand=True)


# ==========================================================
#                       CPU PAGE
# ==========================================================
cpu_frame = tk.Frame(content, bg="#1e1e2e")

# TOTAL CPU GRAPH
cpu_main_frame, cpu_ax, cpu_line, cpu_canvas = create_graph_frame(cpu_frame, "CPU Total %")
cpu_main_frame.pack(fill="x", padx=10, pady=10)

cpu_data = []

# PER-CORE GRAPH
max_cores = min(4, psutil.cpu_count(logical=True))
percore_frame, per_ax, per_line, per_canvas = create_graph_frame(cpu_frame, "CPU Per-Core %")
percore_frame.pack(fill="x", padx=10, pady=10)

per_lines = [per_line]
for _ in range(1, max_cores):
    l, = per_ax.plot([], [], linewidth=1, antialiased=False)
    per_lines.append(l)

per_data = [[] for _ in range(max_cores)]

def update_cpu_page():
    # Total CPU
    cpu = get_cpu_usage()
    cpu_data.append(cpu)
    cpu_data[:] = cpu_data[-40:]
    cpu_line.set_data(range(len(cpu_data)), cpu_data)
    cpu_ax.set_xlim(0, 40)
    cpu_ax.set_ylim(0, 100)
    cpu_canvas.draw()

    # Per-core
    cores = get_cpu_percore()
    for i in range(max_cores):
        per_data[i].append(cores[i])
        per_data[i][:] = per_data[i][-40:]
        per_lines[i].set_data(range(len(per_data[i])), per_data[i])

    per_ax.set_xlim(0, 40)
    per_ax.set_ylim(0, 100)
    per_canvas.draw()

    if current_frame == cpu_frame:
        root.after(1000, update_cpu_page)


# ==========================================================
#                       MEMORY PAGE
# ==========================================================
mem_frame = tk.Frame(content, bg="#1e1e2e")

mem_graph_frame, mem_ax, mem_line, mem_canvas = create_graph_frame(mem_frame, "Memory Usage %")
mem_graph_frame.pack(fill="x", padx=10, pady=10)

mem_data = []

mem_pie_frame, mem_pie_ax, mem_pie_canvas = create_pie_frame(mem_frame, "Memory (GB)")
mem_pie_frame.pack(pady=10)

def update_mem_page():
    percent, used, total = get_memory_usage()

    mem_data.append(percent)
    mem_data[:] = mem_data[-40:]
    mem_line.set_data(range(len(mem_data)), mem_data)
    mem_ax.set_xlim(0, 40)
    mem_ax.set_ylim(0, 100)
    mem_canvas.draw()

    mem_pie_ax.clear()
    mem_pie_ax.pie(
        [used, total - used],
        labels=[f"Used {used:.2f}", f"Free {(total-used):.2f}"],
        autopct="%1.0f%%",
        textprops={'color': 'white'}
    )
    mem_pie_canvas.draw()

    if current_frame == mem_frame:
        root.after(1500, update_mem_page)


# ==========================================================
#                       DISK PAGE
# ==========================================================
disk_frame = tk.Frame(content, bg="#1e1e2e")

disk_graph_frame, disk_ax, disk_line, disk_canvas = create_graph_frame(disk_frame, "Disk Speed KB/s")
disk_graph_frame.pack(fill="x", padx=10, pady=10)

disk_data = []

disk_pie_frame, disk_pie_ax, disk_pie_canvas = create_pie_frame(disk_frame, "Read vs Write")
disk_pie_frame.pack(pady=10)

def update_disk_page():
    r, w = get_disk_speed()

    disk_data.append(r + w)
    disk_data[:] = disk_data[-40:]
    disk_line.set_data(range(len(disk_data)), disk_data)
    disk_ax.set_xlim(0, 40)
    disk_ax.set_ylim(0, max(40, max(disk_data)))
    disk_canvas.draw()

    disk_pie_ax.clear()
    disk_pie_ax.pie(
        [r, w],
        labels=[f"Read {r:.1f}", f"Write {w:.1f}"],
        autopct="%1.0f%%",
        textprops={'color': 'white'}
    )
    disk_pie_canvas.draw()

    if current_frame == disk_frame:
        root.after(1500, update_disk_page)


# ==========================================================
#                       NETWORK PAGE
# ==========================================================
net_frame = tk.Frame(content, bg="#1e1e2e")

net_graph_frame, net_ax, net_line, net_canvas = create_graph_frame(net_frame, "Network KB/s")
net_graph_frame.pack(fill="x", padx=10, pady=10)

net_data = []

def update_net_page():
    d, u = get_network_speed()

    net_data.append(d + u)
    net_data[:] = net_data[-40:]
    net_line.set_data(range(len(net_data)), net_data)
    net_ax.set_xlim(0, 40)
    net_ax.set_ylim(0, max(40, max(net_data)))
    net_canvas.draw()

    if current_frame == net_frame:
        root.after(1200, update_net_page)


# ==========================================================
#                       GPU PAGE
# ==========================================================
gpu_frame = tk.Frame(content, bg="#1e1e2e")

gpu_graph_frame, gpu_ax, gpu_line, gpu_canvas = create_graph_frame(gpu_frame, "GPU Utilization %")
gpu_graph_frame.pack(fill="x", padx=10, pady=10)

gpu_data = []

gpu_pie_frame, gpu_pie_ax, gpu_pie_canvas = create_pie_frame(gpu_frame, "GPU VRAM")
gpu_pie_frame.pack(pady=10)

def update_gpu_page():
    info = get_gpu_usage()
    if info is None:
        gpu_ax.clear()
        gpu_ax.text(0.5, 0.5, "No NVIDIA GPU Detected", ha="center", va="center", color="white")
        gpu_canvas.draw()
        return

    util, used, total = info

    gpu_data.append(util)
    gpu_data[:] = gpu_data[-40:]
    gpu_line.set_data(range(len(gpu_data)), gpu_data)
    gpu_ax.set_xlim(0, 40)
    gpu_ax.set_ylim(0, 100)
    gpu_canvas.draw()

    gpu_pie_ax.clear()
    gpu_pie_ax.pie(
        [used, total-used],
        labels=[f"Used {used/1024:.2f}GB", f"Free {(total-used)/1024:.2f}GB"],
        autopct="%1.0f%%",
        textprops={'color': 'white'}
    )
    gpu_pie_canvas.draw()

    if current_frame == gpu_frame:
        root.after(2000, update_gpu_page)


# ==========================================================
# SIDEBAR BUTTONS
# ==========================================================
btn_cpu = create_sidebar_button(sidebar, "CPU", "🔥", lambda: (activate_button(btn_cpu, buttons), show_frame(cpu_frame), update_cpu_page()))
btn_mem = create_sidebar_button(sidebar, "Memory", "🧠", lambda: (activate_button(btn_mem, buttons), show_frame(mem_frame), update_mem_page()))
btn_disk = create_sidebar_button(sidebar, "Disk", "💾", lambda: (activate_button(btn_disk, buttons), show_frame(disk_frame), update_disk_page()))
btn_net = create_sidebar_button(sidebar, "Network", "🌐", lambda: (activate_button(btn_net, buttons), show_frame(net_frame), update_net_page()))
btn_gpu = create_sidebar_button(sidebar, "GPU", "🎮", lambda: (activate_button(btn_gpu, buttons), show_frame(gpu_frame), update_gpu_page()))

buttons.extend([btn_cpu, btn_mem, btn_disk, btn_net, btn_gpu])

for b in buttons:
    b.pack(fill="x", padx=8, pady=6)

# First page open
activate_button(btn_cpu, buttons)
show_frame(cpu_frame)
update_cpu_page()

root.mainloop()
