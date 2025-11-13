import tkinter as tk

def create_card(root, title, color, row, col):
    card = tk.Frame(root, bg=color, bd=3, relief="ridge")
    card.grid(row=row, column=col, padx=25, pady=25, sticky="nsew")

    title_label = tk.Label(card, text=title, bg=color, fg="white",
                           font=("Arial", 18, "bold"))
    title_label.pack(anchor="w", padx=15, pady=10)

    value_label = tk.Label(card, text="", bg=color, fg="white",
                           font=("Arial", 36, "bold"))
    value_label.pack(anchor="w", padx=20)

    return value_label
