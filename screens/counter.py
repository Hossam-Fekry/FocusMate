from customtkinter import *
import subprocess
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import PIL.Image as Image
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "counted.json")
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")

#make the functions

def plus():
    global number
    number = number + 1
    number_label.configure(text=number)
    save_count(number)

def minus():
    global number
    number = number - 1
    number_label.configure(text=number)
    save_count(number)

def go_back(event = None):    
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])

def load_count():
    with open(DATA_FILE, "r") as file:
        count = json.load(file)
        return count["count"]


def save_count(data):
    with open(DATA_FILE, "w") as file:
        json.dump({"count": data}, file, indent=4)

def load_settings():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["theme"]
    
#make the UI

root = CTk()
root.geometry("450x350")
root.title("FocusMate - Counter")
root.resizable(False, False)
center_window(root, 450, 350)
root.iconbitmap("assets/icons/counter.ico")
set_appearance_mode(load_settings())

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

number = load_count()

CTkLabel(root, text="Counter Screen", font=("Arial", 24,"bold")).pack(pady=30)

number_label = CTkLabel(root, text=number, font=("Arial", 48, "bold"))
number_label.pack(pady=50)

plus_button = CTkButton(root, text="+", command=plus, fg_color="#02960C",hover_color="#015606", text_color="white", font=("Arial", 16, "bold"),corner_radius=25)
plus_button.place(x = 25, y = 160)

minus_button = CTkButton(root, text="-", command=minus, fg_color="#C0392B",hover_color="#A93226", text_color="white", font=("Arial", 16, "bold"),corner_radius=25)
minus_button.place(x = 300, y = 160)

back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)

root.bind('<Escape>', go_back)

root.mainloop()