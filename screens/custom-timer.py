from customtkinter import *
import tkinter as tk
import threading
import time
import os
import json
import subprocess
from PIL import Image
import sys
from plyer import notification
import winsound

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("theme", "dark")
    except Exception:
        return "dark"


def save_progress(minutes: int):
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"sessions": []}
        else:
            data = {"sessions": []}
        import datetime
        today = datetime.date.today().isoformat()
        found = False
        for session in data["sessions"]:
            if session.get("date") == today:
                session["minutes"] = session.get("minutes", 0) + minutes
                found = True
                break
        if not found:
            data["sessions"].append({"date": today, "minutes": minutes})
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass


def go_back():
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])


# State
time_running = False
paused = False
remaining_time = 0
elapsed_seconds = 0


def update_timer_label():
    global remaining_time
    mins, secs = divmod(remaining_time, 60)
    hrs, mins = divmod(mins, 60)
    timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")


def start_timer():
    global time_running, remaining_time, paused
    if time_running:
        return
    paused = False
    try:
        h = int(hours_var.get())
        m = int(minutes_var.get())
        s = int(seconds_var.get())
    except ValueError:
        return
    total = h * 3600 + m * 60 + s
    if total <= 0:
        return
    remaining_time = total
    update_timer_label()
    time_running = True
    threading.Thread(target=run_timer, daemon=True).start()


def run_timer():
    global remaining_time, time_running, paused, elapsed_seconds
    while remaining_time > 0 and time_running:
        if not paused:
            mins, secs = divmod(remaining_time, 60)
            hrs, mins = divmod(mins, 60)
            timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
            time.sleep(1)
            remaining_time -= 1
            elapsed_seconds += 1
        else:
            time.sleep(0.2)
    if remaining_time <= 0 and time_running:
        timer_label.configure(text="00:00:00")
        minutes = elapsed_seconds // 60
        if minutes > 0:
            save_progress(minutes)
        # Play sound and show notification
        winsound.Beep(1000, 1000)  # Beep at 1000Hz for 1 second
        notification.notify(
            title='FocusMate Timer',
            message='Your timer is complete!',
            app_icon='assets/logo.ico',  # Optional icon
            timeout=10  # Notification stays for 10 seconds
        )
        stop_timer()


def pause_timer():
    global paused
    paused = True


def resume_timer():
    global paused
    paused = False


def stop_timer():
    global time_running, paused, remaining_time, elapsed_seconds
    time_running = False
    paused = False
    remaining_time = 0
    elapsed_seconds = 0


def reset_timer():
    stop_timer()
    timer_label.configure(text="00:00:00")


# UI setup
root = CTk()
root.title("FocusMate - Custom Timer")
root.geometry("450x380")
root.resizable(False, False)
center_window(root, 450, 380)
root.iconbitmap("assets/icons/custom-timer.ico")
set_appearance_mode(load_settings())

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back, width=40, height=40)
back_button.place(x=10, y=10)

CTkLabel(root, text="Customized Timer", font=("Arial", 24, "bold")).pack(pady=20)

time_frame = CTkFrame(root)
time_frame.pack(pady=10)

hours_var = tk.StringVar(value="0")
minutes_var = tk.StringVar(value="0")
seconds_var = tk.StringVar(value="0")

CTkEntry(time_frame, textvariable=hours_var, width=70, placeholder_text="hh").grid(row=0, column=0, padx=5)
CTkLabel(time_frame, text="h").grid(row=1, column=0)

CTkEntry(time_frame, textvariable=minutes_var, width=70, placeholder_text="mm").grid(row=0, column=1, padx=5)
CTkLabel(time_frame, text="m").grid(row=1, column=1)

CTkEntry(time_frame, textvariable=seconds_var, width=70, placeholder_text="ss").grid(row=0, column=2, padx=5)
CTkLabel(time_frame, text="s").grid(row=1, column=2)

timer_label = CTkLabel(root, text="00:00:00", font=("Arial", 36, "bold"))
timer_label.pack(pady=20)

btn_frame = CTkFrame(root)
btn_frame.pack(pady=10)

CTkButton(btn_frame, text="Start", fg_color="#02960C", hover_color="#005506", command=start_timer).grid(row=0, column=0, padx=6)
CTkButton(btn_frame, text="Pause", fg_color="#83A400", hover_color="#455600", command=pause_timer).grid(row=0, column=1, padx=6)
CTkButton(btn_frame, text="Resume", fg_color="#1B6CA8", hover_color="#124970", command=resume_timer).grid(row=0, column=2, padx=6)
CTkButton(btn_frame, text="Reset", fg_color="#C0392B", hover_color="#A93226", command=reset_timer).grid(row=0, column=3, padx=6)

root.mainloop()


