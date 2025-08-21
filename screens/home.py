from customtkinter import *
import subprocess
from PIL import Image
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import json

def time_update():
    current_time = time.strftime("%I:%M:%S %p")
    clock_label.configure(text=current_time)
    root.after(1000, time_update)  

def change_screen(screen_name):
    if screen_name == "pomodoro":
        root.destroy()
        subprocess.run(["python", "screens/pomodoro.py"])
    elif screen_name == "todo-list":
        root.destroy()
        subprocess.run(["python", "screens/todo.py"])
    elif screen_name == "statics":
        root.destroy()
        subprocess.run(["python", "screens/stats.py"])
    elif screen_name == "settings":
        root.destroy()
        subprocess.run(["python", "screens/settings.py"])
    elif screen_name == "counter":
        root.destroy()
        subprocess.run(["python", "screens/counter.py"])
    elif screen_name == "custom-timer":
        root.destroy()
        subprocess.run(["python", "screens/custom-timer.py"])
        

def load_settings():
    with open("data/settings.json", "r") as file:
        settings = json.load(file)
        return settings["theme"]

root = CTk()
root.geometry("800x600")
root.title("FocusMate - Home Page")
root.resizable(False, False)
root.iconbitmap("assets/logo.ico")
center_window(root, 800, 600)
set_appearance_mode(load_settings())

CTkLabel(root, text="FocusMate", font=("Arial", 36, "bold")).pack(pady=50)

clock_label = CTkLabel(root, text="", font=("DS-Digital",50, "bold"))
clock_label.pack(pady=100)

time_update()


#load Icons from file system

icons = {
    "counter" : "assets/icons/counter.png",
    "custom-timer" : "assets/icons/custom-timer.png",
    "pomodoro" : "assets/icons/pomodoro-timer.png",
    "todo-list" : "assets/icons/todo-list.png",
    "statics" : "assets/icons/statics.png",
    "settings" : "assets/icons/settings.png"
}


navbar_frame = CTkFrame(root, height=60, fg_color="#1E1E1E")
# navbar_frame.pack(side="bottom", fill="x")

for i, (name, path) in enumerate(icons.items()):
    ico = CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(40, 40))
    
    button = CTkButton(navbar_frame, text="", image=ico, width=50, height=50,fg_color="transparent",hover_color="#333333", command= lambda n = name: change_screen(n))
    button.grid(row=0, column=i, padx=15, pady=5)

navbar_frame.pack(anchor="center",side = BOTTOM, pady=20)
root.mainloop()