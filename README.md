🚀 Real-Time System Monitoring Dashboard

A premium desktop application built using Python + Tkinter, designed to monitor CPU, Memory, Disk, Network, and GPU usage in real-time.
This dashboard provides live graphs, per-core CPU usage, process statistics, and an advanced, modern, task-manager-style UI.
---
🖥️ Features
✔ 1. Real-Time CPU Monitoring

CPU total usage graph

CPU per-core live chart

Top CPU-consuming processes

Rectangle-style process cards for clean UI

✔ 2. Memory Monitoring

Live Memory usage graph

Memory pie-chart breakdown (Used vs Free)

Top memory-consuming processes

✔ 3. Disk Usage

Real-time Disk Read/Write speed chart

Disk Read vs Write pie chart

Top disk-using processes

✔ 4. Network Monitoring

Live upload + download speed graph

Top network-active processes

✔ 5. GPU (NVIDIA) Monitoring

Live GPU utilization graph

VRAM usage pie chart

Auto-detects GPU (hides if no GPU available)

✔ 6. Premium UI

Modern sidebar navigation

Big graphs

Process list in stylish rectangular cards

Smooth animations using fast update cycle

Dark theme

Task-Manager-like layout

---

🏗️ Project Structure
📁 Real-Time-Process-Monitoring-Dashboard
│── Main.py
│── ui.py
│── utils.py
│── README.md
│── monitor.py
│── Monitor 
    │── cpu_monitor.py
    │── disk_monitor.py
    │── memory_monitor.py
    │── network_monitor.py

---

📌 Installation
1️⃣ Clone the project
git clone [https://github.com/saumyamihir/The-Real-Time-Process-Monitoring-Dashboard.git]
cd Real-Time-Monitor

2️⃣ Install required libraries
pip install psutil matplotlib

(Optional for GPU Stats)
pip install nvidia-ml-py3

---

▶️ How to Run

Simply run:

python Main.py

The dashboard window will open automatically.

---

⚙️ How It Works
🔹 ui.py
│── Handles:
│── Graph creation
│── Pie chart creation
│── Sidebar & top bar
│── Premium styling

---

🔹 utils.py
│── Handles:
│── CPU / core stats
│── Memory stats
│── Disk I/O
│── Network speeds
│── GPU utilization (NVIDIA)

---

🔹 Main.py
│── Page switching
│── Live updates
│── Drawing graphs
│── Rectangle-style process cards
│── Combining UI + logic together

---

🧠 Technologies Used

Python

Tkinter (GUI)

Matplotlib (Graphs)

Psutil (System Stats)

NVIDIA NVML (GPU Info)

---

👤 Author

Saumya Mihir
Python Developer | UI Designer | Tech Enthusiast

---

⭐ Contribution

Pull requests are welcome.
Fork → Modify → PR.

---

📄 License

This project is open-source and free to use.
