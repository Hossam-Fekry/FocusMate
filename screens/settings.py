from customtkinter import *
import json
import os
import subprocess
from PIL import Image
import sys
from tkinter import messagebox


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("theme", "dark")
    except Exception:
        return "dark"


def save_settings(theme_value: str, pomodoro_time: int = 25):
    data = {"theme": theme_value,
            "pomodoro_time": pomodoro_time}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def on_theme_change(choice: str):
    save_settings(choice)
    set_appearance_mode(choice)


def on_timer_change(choice):
    try:
        minuts = int(choice)
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["pomodoro_time"] = minuts
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the timer.")

def go_back(event = None):
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])


# UI setup
root = CTk()
root.title("FocusMate - Settings")
root.geometry("400x250")
root.resizable(False, False)
center_window(root, 400, 250)
root.iconbitmap("assets/icons/Settings.ico")

current_theme = load_settings()
set_appearance_mode(current_theme)

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back, width=40, height=40)
back_button.place(x=10, y=10)

CTkLabel(root, text="Settings", font=("Arial", 24, "bold")).pack(pady=30)

content_frame = CTkFrame(root)
content_frame.pack(fill="x", padx=20, pady=10)

CTkLabel(content_frame, text="Theme", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")

theme_menu = CTkOptionMenu(content_frame, values=["dark", "light"], command=on_theme_change)
theme_menu.set(current_theme)
theme_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")


CTkLabel(content_frame, text="Pomodoro Timer (minutes)", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")

timer_entry = CTkEntry(content_frame)
timer_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
with open(SETTINGS_FILE, "r") as file:
    settings = json.load(file)
    timer_entry.insert(0, str(settings.get("pomodoro_time", 25)))

timer_entry.bind("<Return>", lambda event: on_timer_change(timer_entry.get()))

root.bind('<Escape>', go_back)
root.mainloop()


