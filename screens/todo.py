import customtkinter as ctk
import json
import os
from PIL import Image
from screens.base_screen import BaseScreen
from tkinter import BooleanVar

class TodoScreen(BaseScreen):
    def setup_ui(self):
        self.tasks_file = "data/tasks.json"
        self.delete_icon = ctk.CTkImage(Image.open("assets/icons/delete.png"))
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        
        self.tasks = self.load_tasks()

        ctk.CTkLabel(self, text="Todo list", font=("Arial", 28, "bold")).pack(pady=30)

        self.task_entry = ctk.CTkEntry(self, placeholder_text="Add new Task")
        self.task_entry.pack(pady=10, padx=30, fill="x")
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        self.add_button = ctk.CTkButton(self, text="Add Task", command=self.add_task, fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25)
        self.add_button.pack(pady=10)

        self.tasks_frame = ctk.CTkScrollableFrame(self, height=350)
        self.tasks_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        self.refresh_tasks()

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    return json.loads(content) if content else []
            except:
                return []
        return []

    def save_tasks(self):
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            self.tasks.append({"text": task_text, "done": False})
            self.task_entry.delete(0, "end")
            self.save_tasks()
            self.refresh_tasks()

    def toggle_task(self, index, var):
        self.tasks[index]["done"] = var.get()
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.refresh_tasks()

    def refresh_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        if not self.tasks:
            ctk.CTkLabel(self.tasks_frame, text="There is no more Tasks 🎉", font=("Arial", 14, "italic")).pack(pady=10)
            return

        for index, task in enumerate(self.tasks):
            var = BooleanVar(value=task["done"])
            task_row = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
            task_row.pack(fill="x", pady=5, padx=5)

            checkbox = ctk.CTkCheckBox(
                task_row,
                text=task["text"],
                variable=var,
                font=("Arial", 14),
                command=lambda i=index, v=var: self.toggle_task(i, v),
                hover_color="#02960C"
            )
            checkbox.pack(side="left", fill="x", expand=True, padx=5)

            delete_btn = ctk.CTkButton(
                task_row,
                text="",
                image=self.delete_icon,
                width=50,
                fg_color="#650000",
                hover_color="#400000",
                text_color="white",
                font=("Arial", 12, "bold"),
                command=lambda i=index: self.delete_task(i)
            )
            delete_btn.pack(side="right", padx=5)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
