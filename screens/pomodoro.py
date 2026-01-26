from customtkinter import *
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import subprocess
import PIL.Image as Image
import threading
import time
import datetime
from tkinter import messagebox
from plyer import notification
import winsound


SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")
running = False
paused = False

def load_progress():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"sessions": []}

def save_progress(minutes):
    # Load existing data or create new structure
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"sessions": []}
    else:
        data = {"sessions": []}
    today = datetime.date.today().isoformat()
    # Check if today's session exists
    found = False
    for session in data["sessions"]:
        if session["date"] == today:
            session["minutes"] += minutes
            found = True
            break
    if not found:
        # Append new session with date and minutes
        session = {
            "date": today,
            "minutes": minutes
        }
        data["sessions"].append(session)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def update_timer_label():
    mins, secs = divmod(time_left, 60)
    timer_label.configure(text=f"{mins:02d}:{secs:02d}")

# تشغيل المؤقت
def start_timer():
    global running, paused
    if not running:
        running = True
        paused = False
        threading.Thread(target=run_timer, daemon=True).start()

# المؤقت نفسه
def run_timer():
    global time_left, running, paused, elapsed_time
    while running and time_left > 0:
        if not paused:
            time.sleep(1)
            time_left -= 1
            elapsed_time += 1  # Track elapsed time
            update_timer_label()
        else:
            time.sleep(0.2)
    if running and time_left == 0:
        # Timer finished, save progress
        minutes = int(elapsed_time / 60)
        if minutes > 0:
            save_progress(minutes)
        timer_label.configure(text="00:00")
        running = False
        elapsed_time = 0
    if elapsed_time <= 0 and 25 * 60:
        timer_label.configure(text="00:00:00")
        minutes = elapsed_time // 60
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

# إيقاف مؤقت مؤقت (Pause)
def pause_timer():
    global paused
    paused = not paused
    if paused:
        pause_button.configure(text="Resume")
    else:
        pause_button.configure(text="Pause")

def reset_timer():
    global running, elapsed_time, time_left
    running = False
    minutes = int(elapsed_time / 60)
    if minutes > 0:
        save_progress(minutes)
    elapsed_time = 0
    time_left = load_time() * 60  # Reset timer to 25:00
    update_timer_label()

def load_theme():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["theme"]

def load_time():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["pomodoro_time"]


def go_back(event=None):
    global running

    if running:
        user_choice = messagebox.askyesnocancel(
            "Timer is running",
            "The timer is still running. Do you want to keep it running and open the home page?"
        ) 

        if user_choice == None:
            return
        if user_choice == True:
            subprocess.Popen([
                "python",
                os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")
            ])
        if user_choice == False:
            root.destroy()
            subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])
    else:
        root.destroy()
        subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])
    
# ! set the main settings for the pomodoro screen

root = CTk()
root.title("FocusMate - Pomodoro Timer")
root.resizable(False, False)
root.geometry("400x300")
root.attributes('-topmost', True)
center_window(root, 400, 300)
set_appearance_mode(load_theme())
root.iconbitmap("assets/icons/pomodoro-timer.ico")
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
pomodoro_image = CTkImage(dark_image=Image.open("./assets/icons/pomodoro-timer.png"), size=(100, 100))
time_left = load_time() * 60  # Set timer to 25 minutes
elapsed_time = 0  # Add this line to track elapsed time

CTkLabel(root, image=pomodoro_image, text="", font=("Arial", 24, "bold")).pack(pady=20)
timer = "25:00"
timer_label = CTkLabel(root, text=timer, font=("Arial", 40, "bold"))
timer_label.pack(pady=20)

start_button = CTkButton(root, text="Start",  fg_color="#02960C",hover_color="#005506", text_color="white", font=("Arial", 16, "bold"),corner_radius=25, width=80, command=start_timer)
start_button.place(x = 50, y = 260)

pause_button = CTkButton(root, text="Pause",  fg_color="#83A400",hover_color="#455600", text_color="white", font=("Arial", 16, "bold"),corner_radius=25, width=80, command=pause_timer)
pause_button.place(x = 150, y = 260)

reset_button = CTkButton(root, text="Reset",  fg_color="#C0392B",hover_color="#A93226", text_color="white", font=("Arial", 16, "bold"),corner_radius=25, width=80, command=reset_timer)
reset_button.place(x = 250, y = 260)

back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)

update_timer_label()

root.bind('<Escape>', go_back)
root.mainloop()