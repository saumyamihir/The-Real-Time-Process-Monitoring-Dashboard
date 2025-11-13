import tkinter as tk
import psutil

def start_network_monitor():
    root = tk.Tk()
    root.title("Network Speed Monitor")
    root.geometry("500x250")
    root.config(bg="#22d66f")

    label_title = tk.Label(root, text="🌐 Network Speed", bg="#22d66f", fg="white",
                           font=("Arial", 20, "bold"))
    label_title.pack(pady=10)

    label_value = tk.Label(root, bg="#22d66f", fg="white",
                           font=("Arial", 32, "bold"))
    label_value.pack()

    last_up = psutil.net_io_counters().bytes_sent
    last_down = psutil.net_io_counters().bytes_recv

    def update_net():
        nonlocal last_up, last_down
        counters = psutil.net_io_counters()

        upload = (counters.bytes_sent - last_up) / 1024
        download = (counters.bytes_recv - last_down) / 1024

        last_up = counters.bytes_sent
        last_down = counters.bytes_recv

        label_value.config(text=f"{download:.1f} KB/s  |  {upload:.1f} KB/s")
        root.after(1000, update_net)

    update_net()
    root.mainloop()
