from customtkinter import *
import json
import os
import sys
import subprocess
from PIL import Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
GOALS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "goals.json")


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("theme", "dark")
    except Exception:
        return "dark"


def load_goals():
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []
    return []


def save_goals():
    with open(GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(goals, f, ensure_ascii=False, indent=4)


def add_goal():
    text = goal_entry.get().strip()
    if not text:
        return
    goals.append({"text": text, "done": False})
    goal_entry.delete(0, "end")
    save_goals()
    refresh_goals()


def toggle_goal(index: int, var):
    goals[index]["done"] = var.get()
    save_goals()
    refresh_goals()


def delete_goal(index: int):
    goals.pop(index)
    save_goals()
    refresh_goals()


def refresh_goals():
    for widget in goals_frame.winfo_children():
        widget.destroy()
    if not goals:
        CTkLabel(goals_frame, text="No goals yet. Add one!", font=("Arial", 14, "italic")).pack(pady=10)
        return
    for index, goal in enumerate(goals):
        var = BooleanVar(value=goal.get("done", False))
        row = CTkFrame(goals_frame, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=5)
        CTkCheckBox(row, text=goal.get("text", ""), variable=var, command=lambda i=index, v=var: toggle_goal(i, v), font=("Arial", 14)).pack(side="left", fill="x", expand=True, padx=5)
        CTkButton(row, text="Delete", fg_color="#650000", hover_color="#400000", command=lambda i=index: delete_goal(i)).pack(side="right", padx=5)


def go_back():
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])


# UI
root = CTk()
root.title("FocusMate - Goals")
root.geometry("500x600")
root.resizable(False, False)
center_window(root, 500, 600)
root.iconbitmap("assets/icons/Goal.png")
set_appearance_mode(load_settings())

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back, width=40, height=40)
back_button.place(x=10, y=10)

CTkLabel(root, text="Daily Goals", font=("Arial", 28, "bold")).pack(pady=30)

goal_entry = CTkEntry(root, placeholder_text="Add new goal")
goal_entry.pack(pady=10, padx=30, fill="x")

CTkButton(root, text="Add Goal", command=add_goal, fg_color="#02960C", hover_color="#015606").pack(pady=10)

goals_frame = CTkScrollableFrame(root, height=380)
goals_frame.pack(pady=10, padx=20, fill="both", expand=True)

goals = load_goals()
refresh_goals()

root.bind("<Return>", lambda event: add_goal())

root.mainloop()


