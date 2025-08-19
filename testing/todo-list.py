import customtkinter as ctk
import json
import os

# إعداد التطبيق
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FocusMate - To-Do List")
app.geometry("400x500")

# ملف حفظ المهام
TASKS_FILE = "tasks.json"

# تحميل المهام من الملف
if os.path.exists("testing/" + TASKS_FILE):
    with open("testing/" + TASKS_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
else:
    tasks = []

# حفظ المهام في الملف
def save_tasks():
    with open("testing/" + TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

# دالة لإضافة مهمة
def add_task():
    task_text = task_entry.get()
    if task_text:
        tasks.append({"text": task_text, "done": False})
        task_entry.delete(0, "end")
        save_tasks()
        refresh_tasks()

# دالة لتغيير حالة المهمة
def toggle_task(index, var):
    tasks[index]["done"] = var.get()
    save_tasks()

# دالة لحذف مهمة
def delete_task(index):
    tasks.pop(index)
    save_tasks()
    refresh_tasks()

# دالة لتحديث عرض المهام
def refresh_tasks():
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    for index, task in enumerate(tasks):
        var = ctk.BooleanVar(value=task["done"])

        # إطار لكل مهمة مع checkbox وزر حذف
        task_row = ctk.CTkFrame(tasks_frame, fg_color="transparent")
        task_row.pack(fill="x", pady=5, padx=5)

        checkbox = ctk.CTkCheckBox(
            task_row,
            text=task["text"],
            variable=var,
            command=lambda i=index, v=var: toggle_task(i, v)
        )
        checkbox.pack(side="left", fill="x", expand=True)

        delete_btn = ctk.CTkButton(
            task_row,
            text="حذف",
            width=50,
            command=lambda i=index: delete_task(i)
        )
        delete_btn.pack(side="right", padx=5)

# إدخال المهمة
task_entry = ctk.CTkEntry(app, placeholder_text="أضف مهمة جديدة...")
task_entry.pack(pady=20, padx=20, fill="x")

# زر الإضافة
add_button = ctk.CTkButton(app, text="إضافة مهمة", command=add_task)
add_button.pack(pady=10)

# إطار قابل للتمرير لعرض المهام
tasks_frame = ctk.CTkScrollableFrame(app, height=300)
tasks_frame.pack(pady=10, padx=20, fill="both", expand=True)

# عرض المهام عند بدء التطبيق
refresh_tasks()

app.mainloop()
