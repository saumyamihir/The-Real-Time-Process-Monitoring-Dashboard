import tkinter as tk
import psutil

def start_disk_monitor():
    root = tk.Tk()
    root.title("Disk Speed Monitor")
    root.geometry("500x250")
    root.config(bg="#a64ff5")

    label_title = tk.Label(root, text="💾 Disk Speed", bg="#a64ff5", fg="white",
                           font=("Arial", 20, "bold"))
    label_title.pack(pady=10)

    label_value = tk.Label(root, bg="#a64ff5", fg="white",
                           font=("Arial", 32, "bold"))
    label_value.pack()

    last_read = psutil.disk_io_counters().read_bytes
    last_write = psutil.disk_io_counters().write_bytes

    def update_disk():
        nonlocal last_read, last_write
        counters = psutil.disk_io_counters()

        read_speed = (counters.read_bytes - last_read) / 1024
        write_speed = (counters.write_bytes - last_write) / 1024

        last_read = counters.read_bytes
        last_write = counters.write_bytes

        label_value.config(text=f"{read_speed:.1f} KB/s  |  {write_speed:.1f} KB/s")
        root.after(1000, update_disk)

    update_disk()
    root.mainloop()
