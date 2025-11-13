import tkinter as tk
import psutil

def start_cpu_monitor():
    root = tk.Tk()
    root.title("CPU Usage Monitor")
    root.geometry("400x200")
    root.config(bg="#ff3b30")

    label_title = tk.Label(root, text="🔥 CPU Usage", bg="#ff3b30", fg="white",
                           font=("Arial", 20, "bold"))
    label_title.pack(pady=10)

    label_value = tk.Label(root, bg="#ff3b30", fg="white",
                           font=("Arial", 40, "bold"))
    label_value.pack()

    def update_cpu():
        cpu = psutil.cpu_percent()
        label_value.config(text=f"{cpu}%")
        root.after(1000, update_cpu)

    update_cpu()
    root.mainloop()
