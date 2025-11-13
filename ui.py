import tkinter as tk

def create_card(parent, title, color, row, col):
    card = tk.Frame(parent, bg=color, bd=3, relief="ridge")
    card.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")

    title_lbl = tk.Label(card, text=title, bg=color, fg="white",
                         font=("Segoe UI", 16, "bold"))
    title_lbl.pack(anchor="w", padx=10, pady=3)

    value_lbl = tk.Label(card, text="--", bg=color, fg="white",
                         font=("Segoe UI", 28, "bold"))
    value_lbl.pack(anchor="w", padx=10, pady=6)

    return value_lbl
