import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_sidebar_button(root, text, icon, command):
    btn = tk.Button(
        root,
        text=f"{icon}  {text}",
        font=("Arial", 14, "bold"),
        bg="#222",
        fg="white",
        activebackground="#444",
        activeforeground="white",
        bd=0,
        anchor="w",
        padx=15,
        pady=10,
        command=command
    )
    return btn

def activate_button(button, all_buttons):
    for b in all_buttons:
        b.config(bg="#222")
    button.config(bg="#555")

def create_graph_frame(parent, title):
    frame = tk.Frame(parent, bg="#1e1e2e")

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(title, color="white")
    ax.set_facecolor("#222233")
    fig.patch.set_facecolor("#1e1e2e")
    ax.tick_params(colors='white')

    line, = ax.plot([], [], linewidth=2, color="cyan")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return frame, ax, line, canvas
