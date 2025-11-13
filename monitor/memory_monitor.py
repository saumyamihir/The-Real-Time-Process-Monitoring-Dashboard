import tkinter as tk
import psutil

def start_memory_monitor():
    root = tk.Tk()
    root.title("Memory Usage Monitor")
    root.geometry("400x200")
    root.config(bg="#1e90ff")

    label_title = tk.Label(root, text="🧩 Memory Usage", bg="#1e90ff", fg="white",
                           font=("Arial", 20, "bold"))
    label_title.pack(pady=10)

    label_value = tk.Label(root, bg="#1e90ff", fg="white",
                           font=("Arial", 40, "bold"))
    label_value.pack()

    def update_memory():
        mem = psutil.virtual_memory().percent
        label_value.config(text=f"{mem}%")
        root.after(1000, update_memory)

    update_memory()
    root.mainloop()
