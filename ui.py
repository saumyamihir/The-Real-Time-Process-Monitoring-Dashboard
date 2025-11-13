import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ---------- Card Creator ----------
def create_card(root, title, color, row, col):
    card = tk.Frame(root, bg=color, bd=3, relief="ridge")
    card.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")

    title_label = tk.Label(card, text=title, bg=color, fg="white",
                           font=("Arial", 18, "bold"))
    title_label.pack(anchor="w", padx=15, pady=8)

    value_label = tk.Label(card, text="", bg=color, fg="white",
                           font=("Arial", 32, "bold"))
    value_label.pack(anchor="w", padx=20)

    return card, value_label

# ---------- Graph Creator ----------
def create_graph(root, title):
    frame = tk.Frame(root, bg="#1e1e2e")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    fig = Figure(figsize=(5, 2), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(title, color="white")
    ax.set_facecolor("#222233")
    fig.patch.set_facecolor("#1e1e2e")
    ax.tick_params(colors='white')

    line, = ax.plot([], [], linewidth=2)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return ax, line, canvas
