from customtkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import datetime
import sys
from PIL import Image
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data.get("sessions", [])
            except json.JSONDecodeError:
                return []
    return []

def get_stats_by_date(sessions):
    stats = {}
    for session in sessions:
        date = session.get("date")
        minutes = session.get("minutes", 0)
        if date:
            stats[date] = stats.get(date, 0) + minutes
    return stats

def draw_bar_chart(frame, stats):
    # Clear previous chart if any
    for widget in frame.winfo_children():
        widget.destroy()
    if not stats:
        CTkLabel(frame, text="No data to display.", font=("Arial", 16)).pack(pady=20)
        return

    labels = list(stats.keys())
    sizes = list(stats.values())

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.bar(labels, sizes, color="#02960C")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Date")
    ax.set_title("Pomodoro Minutes by Date")
    plt.xticks(rotation=30, ha='right')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plt.close(fig)

def refresh_chart():
    sessions = load_progress()
    stats = get_stats_by_date(sessions)
    draw_bar_chart(chart_frame, stats)

def go_back():
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])

# UI setup
root = CTk()
root.title("FocusMate - Statistics")
root.geometry("600x550")
center_window(root, 600, 500)
root.resizable(False, False)
root.iconbitmap("assets/logo.ico")

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)
CTkLabel(root, text="Pomodoro Statistics", font=("Arial", 28, "bold")).pack(pady=20)

chart_frame = CTkFrame(root)
chart_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

refresh_chart()  # Show bar chart

root.mainloop()
