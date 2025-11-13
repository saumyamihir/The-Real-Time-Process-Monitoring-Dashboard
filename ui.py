import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sidebar button
def create_sidebar_button(root, text, command):
    return tk.Button(
        root,
        text=text,
        font=("Arial", 14, "bold"),
        bg="#333",
        fg="white",
        activebackground="#555",
        activeforeground="white",
        bd=0,
        command=command
    )

# Graph frame creator
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
