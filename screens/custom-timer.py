from customtkinter import *
import tkinter as tk
import os
import json
import subprocess
from PIL import Image
import sys
from plyer import notification
import winsound
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")
home_opened = False

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


# State
time_running = False
paused = False
remaining_time = 0
elapsed_seconds = 0


# ---------------- FIXED go_back (NO CRASH) -----------------
def go_back(event=None):
    global time_running, home_opened

    if time_running:
        user_choice = messagebox.askyesnocancel(
            "Timer is running",
            "The timer is still running. Do you want to keep it running and open the home page?"
        ) 

        if user_choice == None:
            return
        if user_choice == True:
            if home_opened:
                messagebox.showinfo("Home Page", "The home page is already open.")
                return
            else:
                subprocess.Popen([
                "python",
                os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")
                ])
                home_opened = True
        if user_choice == False:
            root.destroy()
            if not home_opened:
                subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])
                home_opened = True
            else:
                return
    else:
        root.destroy()
        if not home_opened:
            subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])
            home_opened = True
        else:
            return


def update_timer_label():
    global remaining_time
    if not root.winfo_exists():  # prevent crash if window closed
        return

    mins, secs = divmod(remaining_time, 60)
    hrs, mins = divmod(mins, 60)
    timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")


def start_timer():
    global time_running, remaining_time, paused
    if time_running:
        return
    paused = False
    # try:
    #     h = int(hours_var.get())
    #     m = int(minutes_var.get())
    #     s = int(seconds_var.get())
    # except ValueError:
    #     return
    # h = hours_var.get().strip()
    # m = minutes_var.get().strip()
    # s = seconds_var.get().strip()
    # if h == "":
    #     h = 0
    # if m == "":
    #     m = 0
    # if s == "":
    #     s = 0


    # if not h.isdigit() or not m.isdigit() or not s.isdigit():
    #     messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")
    #     return

    # h = int(h)
    # m = int(m)
    # s = int(s)

    h = hours_var.get().strip()
    m = minutes_var.get().strip()
    s = seconds_var.get().strip()

    if h == "":
        h = "0"
    if m == "":
        m = "0"
    if s == "":
        s = "0"

    # ✅ validate BEFORE converting
    if not h.isdigit() or not m.isdigit() or not s.isdigit():
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")
        return

    # ✅ now convert
    h = int(h)
    m = int(m)
    s = int(s)

    
    if int(m)  > 240:
        messagebox.showerror("Invalid Input", "For your health please choose lower time to stay focused you limit is 4 hours.")
        return
    if int(h) > 4:
        messagebox.showerror("Invalid Input", "For your health please choose lower time to stay focused you limit is 4 hours.")
        return
    if int(s) > 14400:
        messagebox.showerror("Invalid Input", "Seconds should be less than 3600.")
        return
    total = int(h)*3600 + int(m)*60 + int(s)
    if total > 14400:
        messagebox.showerror("Invalid Input", "Total time should be less than 4 hours.")
        return
    total = int(h)*3600 + int(m)*60 + int(s)
    if total <= 0:
        return

    remaining_time = total
    time_running = True
    hours_entry.configure(state="disabled")
    minutes_entry.configure(state="disabled")
    seconds_entry.configure(state="disabled")
    start_button.configure(state="disabled")

    update_timer_background()

def update_timer_background():
    global remaining_time, time_running, paused, elapsed_seconds

    if not time_running:
        return

    if not paused:
        mins, secs = divmod(remaining_time, 60)
        hrs, mins = divmod(mins, 60)
        try:
            timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")
        except:
            return

        remaining_time -= 1
        elapsed_seconds += 1

        # Save progress every 60 seconds
        if elapsed_seconds % 60 == 0:
            minutes = elapsed_seconds // 60
            save_progress(minutes)

        if remaining_time <= 0:
            # Timer finished
            minutes = elapsed_seconds // 60
            if minutes > 0:
                save_progress(minutes)
            winsound.Beep(1000,1000)
            notification.notify(
                title='FocusMate Timer',
                message='Your timer is complete!',
                app_icon='assets/logo.ico',
                timeout=10
            )
            hours_entry.configure(state="normal")
            minutes_entry.configure(state="normal")
            seconds_entry.configure(state="normal")
            start_button.configure(state="normal")
            stop_timer()
            return

    # إعادة استدعاء الدالة بعد ثانية
    root.after(1000, update_timer_background)

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
    global elapsed_seconds, time_running
    minutes = elapsed_seconds // 60
    if minutes > 0:
        save_progress(minutes)
    stop_timer()
    timer_label.configure(text="00:00:00")


# ----------------- UI -----------------
root = CTk()
root.title("FocusMate - Custom Timer")
root.geometry("610x380")
center_window(root, 610, 380)
root.iconbitmap("assets/icons/custom-timer.ico")
set_appearance_mode(load_settings())
root.attributes('-topmost', True)


back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon,
                        fg_color="transparent", hover_color="#333333",
                        command=go_back, width=40, height=40)
back_button.place(x=10, y=10)

CTkLabel(root, text="Customized Timer", font=("Arial", 24, "bold")).pack(pady=20)

time_frame = CTkFrame(root)
time_frame.pack(pady=10)

hours_var = tk.StringVar(value="0")
minutes_var = tk.StringVar(value="0")
seconds_var = tk.StringVar(value="0")

hours_entry = CTkEntry(time_frame, textvariable=hours_var, width=70)
hours_entry.grid(row=0, column=0, padx=5)
CTkLabel(time_frame, text="h").grid(row=1, column=0)

minutes_entry = CTkEntry(time_frame, textvariable=minutes_var, width=70)
minutes_entry.grid(row=0, column=1, padx=5)
CTkLabel(time_frame, text="m").grid(row=1, column=1)

seconds_entry = CTkEntry(time_frame, textvariable=seconds_var, width=70)
seconds_entry.grid(row=0, column=2, padx=5)
CTkLabel(time_frame, text="s").grid(row=1, column=2)

timer_label = CTkLabel(root, text="00:00:00", font=("Arial", 36, "bold"))
timer_label.pack(pady=20)

btn_frame = CTkFrame(root)
btn_frame.pack(pady=10)

start_button = CTkButton(btn_frame, text="Start", fg_color="#02960C", hover_color="#005506",
          command=start_timer)
start_button.grid(row=0, column=0, padx=6)

pause_button = CTkButton(btn_frame, text="Pause", fg_color="#83A400", hover_color="#455600",
          command=pause_timer)
pause_button.grid(row=0, column=1, padx=6)

resume_button = CTkButton(btn_frame, text="Resume", fg_color="#1B6CA8", hover_color="#124970",
          command=resume_timer)
resume_button.grid(row=0, column=2, padx=6)

reset_button = CTkButton(btn_frame, text="Reset", fg_color="#C0392B", hover_color="#A93226",
          command=reset_timer)
reset_button.grid(row=0, column=3, padx=6)


root.bind('<Escape>', go_back)
root.mainloop()
