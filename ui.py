import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================= TOP BAR =================
def create_topbar(root, title):
    bar = tk.Frame(root, bg="#000000", height=50)
    bar.pack(fill="x")

    tk.Label(
        bar, text=title,
        font=("Arial", 20, "bold"),
        fg="cyan", bg="#000000"
    ).pack(side="left", padx=20)


# ================= SIDEBAR =================
def create_sidebar_button(root, text, icon, command):
    return tk.Button(
        root,
        text=f"{icon}  {text}",
        bg="#222", fg="white",
        activebackground="#555",
        bd=0, anchor="w",
        padx=15, pady=10,
        font=("Arial", 14, "bold"),
        command=command
    )

def activate_button(selected, group):
    for btn in group:
        btn.config(bg="#222")
    selected.config(bg="#444")


# ================== SMALL GRAPH FRAME ==================
def create_graph_frame(parent, title):
    """
    Returns: frame, ax, line, canvas
    """

    frame = tk.Frame(parent, bg="#1e1e2e")

    fig = Figure(figsize=(4, 2), dpi=100)    # <<< SMALL GRAPH HERE
    ax = fig.add_subplot(111)
    ax.set_title(title, color="white")
    ax.set_facecolor("#202025")
    fig.patch.set_facecolor("#1e1e2e")
    ax.tick_params(colors='white', labelsize=8)

    line, = ax.plot([], [], linewidth=2, antialiased=False, color="cyan")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="x", expand=False)

    return frame, ax, line, canvas


# ================= PIE FRAME ==================
def create_pie_frame(parent, title):
    """
    Returns: frame, ax, canvas
    """

    frame = tk.Frame(parent, bg="#1e1e2e")

    fig = Figure(figsize=(3, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(title, color="white")
    fig.patch.set_facecolor("#1e1e2e")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

    return frame, ax, canvas
