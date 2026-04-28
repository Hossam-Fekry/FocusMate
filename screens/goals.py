import customtkinter as ctk
import json
import os
from PIL import Image
from screens.base_screen import BaseScreen
from tkinter import BooleanVar

class GoalsScreen(BaseScreen):
    def setup_ui(self):
        self.goals_file = "data/goals.json"
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        
        self.goals = self.load_goals()

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, fg_color="transparent", hover_color="#333333", command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        ctk.CTkLabel(self, text="Daily Goals", font=("Arial", 28, "bold")).pack(pady=30)

        self.goal_entry = ctk.CTkEntry(self, placeholder_text="Add new goal")
        self.goal_entry.pack(pady=10, padx=30, fill="x")
        self.goal_entry.bind("<Return>", lambda e: self.add_goal())

        ctk.CTkButton(self, text="Add Goal", command=self.add_goal, fg_color="#02960C", hover_color="#015606").pack(pady=10)

        self.goals_frame = ctk.CTkScrollableFrame(self, height=380)
        self.goals_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.refresh_goals()

    def load_goals(self):
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    return json.loads(content) if content else []
            except: return []
        return []

    def save_goals(self):
        with open(self.goals_file, "w", encoding="utf-8") as f:
            json.dump(self.goals, f, indent=4)

    def add_goal(self):
        text = self.goal_entry.get().strip()
        if text:
            self.goals.append({"text": text, "done": False})
            self.goal_entry.delete(0, "end")
            self.save_goals()
            self.refresh_goals()

    def toggle_goal(self, index, var):
        self.goals[index]["done"] = var.get()
        self.save_goals()
        self.refresh_goals()

    def delete_goal(self, index):
        self.goals.pop(index)
        self.save_goals()
        self.refresh_goals()

    def refresh_goals(self):
        for widget in self.goals_frame.winfo_children():
            widget.destroy()
        
        if not self.goals:
            ctk.CTkLabel(self.goals_frame, text="No goals yet.", font=("Arial", 14, "italic")).pack(pady=10)
            return

        for index, goal in enumerate(self.goals):
            var = BooleanVar(value=goal.get("done", False))
            row = ctk.CTkFrame(self.goals_frame, fg_color="transparent")
            row.pack(fill="x", pady=5, padx=5)
            ctk.CTkCheckBox(row, text=goal.get("text", ""), variable=var, command=lambda i=index, v=var: self.toggle_goal(i, v)).pack(side="left", fill="x", expand=True, padx=5)
            ctk.CTkButton(row, text="Delete", width=60, fg_color="#650000", hover_color="#400000", command=lambda i=index: self.delete_goal(i)).pack(side="right", padx=5)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
