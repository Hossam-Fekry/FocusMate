from customtkinter import *
import json
import os
import sys
import PIL.Image as Image
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import subprocess

# إعداد التطبيق
def load_settings():
    with open("data/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)
        return settings.get("theme", "Light")

set_appearance_mode(load_settings())
set_default_color_theme("green")

root = CTk()
root.title("FocusMate - To-Do List")
root.geometry("500x600")
root.resizable(False, False)
center_window(root, 500, 600)
root.iconbitmap("assets/logo.ico")
delete_icon = CTkImage(Image.open("assets/icons/delete.png"))
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
# ملف حفظ المهام
TASKS_FILE = "data/tasks.json"

# تحميل المهام من الملف
tasks = []
if os.path.exists(TASKS_FILE):
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                tasks = json.loads(content)
            else:
                tasks = []
    except json.JSONDecodeError:
        tasks = []
else:
    tasks = []

# حفظ المهام في الملف
def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# دالة لإضافة مهمة
def add_task():
    task_text = task_entry.get().strip()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        task_entry.delete(0, "end")
        save_tasks()
        refresh_tasks()

# دالة لتغيير حالة المهمة
def toggle_task(index, var):
    tasks[index]["done"] = var.get()
    save_tasks()
    refresh_tasks()

# دالة لحذف مهمة
def delete_task(index):
    tasks.pop(index)
    save_tasks()
    refresh_tasks()

# دالة لتحديث عرض المهام
def refresh_tasks():
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    if not tasks:
        CTkLabel(tasks_frame, text="There is no more Tasks 🎉", font=("Arial", 14, "italic")).pack(pady=10)
        return

    for index, task in enumerate(tasks):
        var = BooleanVar(value=task["done"])

        # إطار لكل مهمة مع checkbox وزر حذف
        task_row = CTkFrame(tasks_frame, fg_color="transparent")
        task_row.pack(fill="x", pady=5, padx=5)

        checkbox = CTkCheckBox(
            task_row,
            text=task["text"],
            variable=var,
            font=("Arial", 14),
            command=lambda i=index, v=var: toggle_task(i, v),
            hover_color="#02960C"
        )
        checkbox.pack(side="left", fill="x", expand=True, padx=5)

        delete_btn = CTkButton(
            task_row,
            text="",
            image=delete_icon,
            width=50,
            fg_color="#650000",
            hover_color="#400000",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=lambda i=index: delete_task(i)
        )
        delete_btn.pack(side="right", padx=5)

def go_back():
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])

# عنوان الصفحة
CTkLabel(root, text="Todo list", font=("Arial", 28, "bold")).pack(pady=30)

# إدخال المهمة
task_entry = CTkEntry(root, placeholder_text="Add new Task")
task_entry.pack(pady=10, padx=30, fill="x")

# زر الإضافة
add_button = CTkButton(root, text="Add Task", command=add_task,fg_color="#02960C",hover_color="#015606", text_color="white", font=("Arial", 16, "bold"),corner_radius=25)
add_button.pack(pady=10)

# إطار قابل للتمرير لعرض المهام
tasks_frame = CTkScrollableFrame(root, height=350)
tasks_frame.pack(pady=10, padx=20, fill="both", expand=True)

back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)
# عرض المهام عند بدء التطبيق
refresh_tasks()

root.bind("<Return>", lambda event: add_task())

root.mainloop()
