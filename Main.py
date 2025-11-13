import tkinter as tk
from ui import create_card
from monitor import get_usage

root = tk.Tk()
root.title("Real Time Process Monitoring Dashboard")
root.state("zoomed")
root.config(bg="#1e1e2e")

grid_frame = tk.Frame(root, bg="#1e1e2e")
grid_frame.pack(fill="both", expand=True)

grid_frame.grid_columnconfigure(0, weight=1)
grid_frame.grid_columnconfigure(1, weight=1)
grid_frame.grid_rowconfigure(0, weight=1)
grid_frame.grid_rowconfigure(1, weight=1)

cpu_lbl = create_card(grid_frame, "🔥 CPU Usage", "#ff4141", 0, 0)
mem_lbl = create_card(grid_frame, "📘 Memory Usage", "#43a2ff", 0, 1)
disk_lbl = create_card(grid_frame, "💾 Disk Speed", "#b043ff", 1, 0)
net_lbl = create_card(grid_frame, "🌐 Network Speed", "#39ff85", 1, 1)

def update_dashboard():
    data = get_usage()

    cpu_lbl.config(text=f"{data['cpu']}%")
    mem_lbl.config(text=f"{data['mem']}%")

    disk_lbl.config(text=f"{data['read']:.1f} KB/s | {data['write']:.1f} KB/s")
    net_lbl.config(text=f"{data['upload']:.1f} KB/s | {data['download']:.1f} KB/s")

    root.after(2000, update_dashboard)

tk.Label(root, text="⚙ Processes Status Dashboard",
         fg="white", bg="#1e1e2e",
         font=("Segoe UI", 26, "bold")
         ).pack(pady=10)

update_dashboard()
root.mainloop()
