from customtkinter import *
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import subprocess
import PIL.Image as Image
import threading
import time

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")
running = False
paused = False
time_left = 25 * 60

def load_progress():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"sessions": []}

def save_progress(hours):
    data = load_progress()
    data["sessions"].append(hours)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

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
    global time_left, running, paused
    while running and time_left > 0:
        if not paused:
            time.sleep(1)
            time_left -= 1
            update_timer_label()
        else:
            time.sleep(0.2)

# إيقاف مؤقت مؤقت (Pause)
def pause_timer():
    global paused
    paused = not paused
    if paused:
        pause_button.configure(text="Resume")
    else:
        pause_button.configure(text="Pause")

def reset_timer():
    global running, elapsed_time
    running = False
    if elapsed_time > 0:
        minutes = elapsed_time / 60
        hours = round(minutes / 60, 2)
        save_progress(hours)  # حفظ التقدم بعد ما يخلص
    elapsed_time = 0
    timer_label.config(text="00:00")

def load_settings():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["theme"]

def go_back():
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])

root = CTk()
root.title("FocusMate - Pomodoro Timer")
root.resizable(False, False)
root.geometry("400x300")
center_window(root, 400, 300)
set_appearance_mode(load_settings())
root.iconbitmap("assets/icons/pomodoro-timer.ico")
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
pomodoro_image = CTkImage(dark_image=Image.open("./assets/icons/pomodoro-timer.png"), size=(100, 100))
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

root.mainloop()