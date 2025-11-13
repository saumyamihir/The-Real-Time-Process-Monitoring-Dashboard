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

# =================== MAIN WINDOW ===================
root = tk.Tk()
root.title("Real-Time Process Monitoring Dashboard")
root.geometry("1360x850")
root.config(bg="#1e1e2e")

create_topbar(root, "🔥 Real-Time Process Monitoring Dashboard")

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

# LEFT SIDE (graphs)
cpu_left = tk.Frame(cpu_frame, bg="#1e1e2e")
cpu_left.pack(side="left", fill="both", expand=True, padx=25, pady=25)

cpu_main_frame, cpu_ax, cpu_line, cpu_canvas = create_graph_frame(cpu_left, "CPU Total Usage %")
cpu_main_frame.pack(pady=12)

cpu_data = []

max_cores = min(4, psutil.cpu_count(logical=True))
percore_frame, per_ax, per_line, per_canvas = create_graph_frame(cpu_left, "CPU Per-Core Usage %")
percore_frame.pack(pady=12)

per_lines = [per_line]
for _ in range(1, max_cores):
    ln, = per_ax.plot([], [], linewidth=1, antialiased=False)
    per_lines.append(ln)

per_data = [[] for _ in range(max_cores)]

# RIGHT SIDE (Process list)
cpu_proc_frame = tk.Frame(
    cpu_frame, bg="#111", width=36,
    relief="ridge", bd=3,
    highlightbackground="#444",
    highlightcolor="#444",
    highlightthickness=2
)
cpu_proc_frame.pack(side="right", fill="y", padx=55, pady=45, anchor="n")

tk.Label(cpu_proc_frame, text="Top CPU Processes",
         font=("Arial", 16, "bold"), fg="cyan", bg="#111").pack(pady=12)

cpu_process_list = tk.Listbox(cpu_proc_frame, font=("Consolas", 12),
                              bg="#222", fg="white", width=36)
cpu_process_list.pack(fill="both", expand=True, padx=12, pady=12)


def update_cpu_page():
    # CPU total graph
    cpu = get_cpu_usage()
    cpu_data.append(cpu)
    cpu_data[:] = cpu_data[-40:]
    cpu_line.set_data(range(len(cpu_data)), cpu_data)
    cpu_ax.set_xlim(0, 40)
    cpu_ax.set_ylim(0, 100)
    cpu_canvas.draw()

    # Per-core graph
    core_vals = get_cpu_percore()
    for i in range(max_cores):
        per_data[i].append(core_vals[i])
        per_data[i][:] = per_data[i][-40:]
        per_lines[i].set_data(range(len(per_data[i])), per_data[i])
    per_ax.set_xlim(0, 40)
    per_ax.set_ylim(0, 100)
    per_canvas.draw()

    # Process list
    cpu_process_list.delete(0, tk.END)
    processes = []

    for p in psutil.process_iter(['name', 'pid', 'cpu_percent']):
        try:
            processes.append((p.info['cpu_percent'], p.info['name'], p.info['pid']))
        except:
            pass

    processes = sorted(processes, reverse=True)[:12]

    for cpu_use, name, pid in processes:
        cpu_process_list.insert(
            tk.END,
            f"{cpu_use:5.1f}% | {name[:18]:18} | PID {pid}"
        )

    if current_frame == cpu_frame:
        root.after(1000, update_cpu_page)


# ==========================================================
#                     MEMORY PAGE
# ==========================================================
mem_frame = tk.Frame(content, bg="#1e1e2e")

mem_left = tk.Frame(mem_frame, bg="#1e1e2e")
mem_left.pack(side="left", fill="both", expand=True, padx=25, pady=25)

mem_graph_frame, mem_ax, mem_line, mem_canvas = create_graph_frame(mem_left, "Memory Usage %")
mem_graph_frame.pack(pady=12)

mem_data = []

mem_pie_frame, mem_pie_ax, mem_pie_canvas = create_pie_frame(mem_left, "Memory Breakdown")
mem_pie_frame.pack(pady=12)

mem_proc_frame = tk.Frame(
    mem_frame, bg="#111", width=360,
    relief="ridge", bd=3,
    highlightbackground="#444",
    highlightcolor="#444",
    highlightthickness=2
)
mem_proc_frame.pack(side="right", fill="y", padx=55, pady=45, anchor="n")

tk.Label(mem_proc_frame, text="Top Memory Processes",
         font=("Arial", 16, "bold"), fg="cyan", bg="#111").pack(pady=12)

mem_process_list = tk.Listbox(mem_proc_frame, font=("Consolas", 12),
                              bg="#222", fg="white", width=36)
mem_process_list.pack(fill="both", expand=True, padx=12, pady=12)


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
        labels=[f"Used {used:.2f}GB", f"Free {(total-used):.2f}GB"],
        autopct="%1.0f%%", textprops={'color': 'white'}
    )
    mem_pie_canvas.draw()

    mem_process_list.delete(0, tk.END)
    processes = []

    for p in psutil.process_iter(['name', 'pid', 'memory_info']):
        try:
            mem_used = p.info['memory_info'].rss / (1024**2)
            processes.append((mem_used, p.info['name'], p.info['pid']))
        except:
            pass

    processes = sorted(processes, reverse=True)[:12]

    for mem_mb, name, pid in processes:
        mem_process_list.insert(
            tk.END,
            f"{mem_mb:6.1f} MB | {name[:18]:18} | PID {pid}"
        )

    if current_frame == mem_frame:
        root.after(1200, update_mem_page)


# ==========================================================
#                     DISK PAGE
# ==========================================================
disk_frame = tk.Frame(content, bg="#1e1e2e")

disk_left = tk.Frame(disk_frame, bg="#1e1e2e")
disk_left.pack(side="left", fill="both", expand=True, padx=25, pady=25)

disk_graph_frame, disk_ax, disk_line, disk_canvas = create_graph_frame(disk_left, "Disk Speed KB/s")
disk_graph_frame.pack(pady=12)

disk_pie_frame, disk_pie_ax, disk_pie_canvas = create_pie_frame(disk_left, "Disk Read/Write")
disk_pie_frame.pack(pady=12)

disk_proc_frame = tk.Frame(
    disk_frame, bg="#111", width=360,
    relief="ridge", bd=3,
    highlightbackground="#444",
    highlightcolor="#444",
    highlightthickness=2
)
disk_proc_frame.pack(side="right", fill="y", padx=55, pady=45, anchor="n")

tk.Label(disk_proc_frame, text="Top Disk Processes",
         font=("Arial", 16, "bold"), fg="cyan", bg="#111").pack(pady=12)

disk_process_list = tk.Listbox(disk_proc_frame, font=("Consolas", 12),
                               bg="#222", fg="white", width=36)
disk_process_list.pack(fill="both", expand=True, padx=12, pady=12)

disk_data = []


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
        labels=[f"Read {r:.1f} KB", f"Write {w:.1f} KB"],
        autopct="%1.0f%%", textprops={'color': 'white'}
    )
    disk_pie_canvas.draw()

    disk_process_list.delete(0, tk.END)
    processes = []

    for p in psutil.process_iter(['name', 'pid', 'io_counters']):
        try:
            io = p.info['io_counters']
            total_io = (io.read_bytes + io.write_bytes)
            processes.append((total_io, p.info['name'], p.info['pid']))
        except:
            pass

    processes = sorted(processes, reverse=True)[:12]

    for speed, name, pid in processes:
        disk_process_list.insert(
            tk.END,
            f"{speed/1024/1024:6.2f} MB | {name[:18]:18} | PID {pid}"
        )

    if current_frame == disk_frame:
        root.after(1500, update_disk_page)


# ==========================================================
#                     NETWORK PAGE
# ==========================================================
net_frame = tk.Frame(content, bg="#1e1e2e")

net_left = tk.Frame(net_frame, bg="#1e1e2e")
net_left.pack(side="left", fill="both", expand=True, padx=25, pady=25)

net_graph_frame, net_ax, net_line, net_canvas = create_graph_frame(net_left, "Network Usage KB/s")
net_graph_frame.pack(pady=12)

net_proc_frame = tk.Frame(
    net_frame, bg="#111", width=360,
    relief="ridge", bd=3,
    highlightbackground="#444",
    highlightcolor="#444",
    highlightthickness=2
)
net_proc_frame.pack(side="right", fill="y", padx=55, pady=45, anchor="n")

tk.Label(net_proc_frame, text="Top Network Processes",
         font=("Arial", 16, "bold"), fg="cyan", bg="#111").pack(pady=12)

net_process_list = tk.Listbox(net_proc_frame, font=("Consolas", 12),
                              bg="#222", fg="white", width=36)
net_process_list.pack(fill="both", expand=True, padx=12, pady=12)

net_data = []


def update_net_page():
    d, u = get_network_speed()
    net_data.append(d + u)
    net_data[:] = net_data[-40:]
    net_line.set_data(range(len(net_data)), net_data)
    net_ax.set_xlim(0, 40)
    net_ax.set_ylim(0, max(40, max(net_data)))
    net_canvas.draw()

    net_process_list.delete(0, tk.END)
    processes = []

    for p in psutil.process_iter(['name', 'pid', 'io_counters']):
        try:
            io = p.info['io_counters']
            nw = (io.read_bytes + io.write_bytes) / 1024
            processes.append((nw, p.info['name'], p.info['pid']))
        except:
            pass

    processes = sorted(processes, reverse=True)[:12]

    for net_kb, name, pid in processes:
        net_process_list.insert(
            tk.END,
            f"{net_kb:6.1f} KB | {name[:18]:18} | PID {pid}"
        )

    if current_frame == net_frame:
        root.after(1200, update_net_page)


# ==========================================================
#                     GPU PAGE
# ==========================================================
gpu_frame = tk.Frame(content, bg="#1e1e2e")

gpu_graph_frame, gpu_ax, gpu_line, gpu_canvas = create_graph_frame(gpu_frame, "GPU Utilization %")
gpu_graph_frame.pack(pady=12)

gpu_pie_frame, gpu_pie_ax, gpu_pie_canvas = create_pie_frame(gpu_frame, "GPU VRAM Info")
gpu_pie_frame.pack(pady=12)

gpu_data = []


def update_gpu_page():
    info = get_gpu_usage()
    if info is None:
        gpu_ax.clear()
        gpu_ax.text(0.5, 0.5, "No NVIDIA GPU Detected", ha="center", color="white")
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
        labels=[f"Used {used/1024:.2f} GB", f"Free {(total-used)/1024:.2f} GB"],
        autopct="%1.0f%%",
        textprops={'color': 'white'}
    )
    gpu_pie_canvas.draw()

    if current_frame == gpu_frame:
        root.after(1500, update_gpu_page)


# ================= SIDEBAR BUTTONS ==================

btn_cpu = create_sidebar_button(sidebar, "CPU", "🔥",
                                lambda: (activate_button(btn_cpu, buttons), show_frame(cpu_frame), update_cpu_page()))
btn_mem = create_sidebar_button(sidebar, "Memory", "🧠",
                                lambda: (activate_button(btn_mem, buttons), show_frame(mem_frame), update_mem_page()))
btn_disk = create_sidebar_button(sidebar, "Disk", "💾",
                                 lambda: (activate_button(btn_disk, buttons), show_frame(disk_frame), update_disk_page()))
btn_net = create_sidebar_button(sidebar, "Network", "🌐",
                                lambda: (activate_button(btn_net, buttons), show_frame(net_frame), update_net_page()))
btn_gpu = create_sidebar_button(sidebar, "GPU", "🎮",
                                lambda: (activate_button(btn_gpu, buttons), show_frame(gpu_frame), update_gpu_page()))

buttons.extend([btn_cpu, btn_mem, btn_disk, btn_net, btn_gpu])

for b in buttons:
    b.pack(fill="x", padx=10, pady=10)

activate_button(btn_cpu, buttons)
show_frame(cpu_frame)
update_cpu_page()

root.mainloop()
