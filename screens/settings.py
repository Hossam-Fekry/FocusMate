import customtkinter as ctk
import json
import os
from PIL import Image
from tkinter import messagebox
from screens.base_screen import BaseScreen

class SettingsScreen(BaseScreen):
    def setup_ui(self):
        self.settings_file = "data/settings.json"
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        
        current_theme = self.controller.settings.get("theme", "dark")
        
        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        ctk.CTkLabel(self, text="Settings", font=("Arial", 24, "bold")).pack(pady=30)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.content_frame, text="Theme", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_menu = ctk.CTkOptionMenu(self.content_frame, values=["dark", "light"], command=self.on_theme_change)
        self.theme_menu.set(current_theme)
        self.theme_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.content_frame, text="Pomodoro Timer (min)", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.timer_entry = ctk.CTkEntry(self.content_frame)
        self.timer_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.timer_entry.insert(0, str(self.controller.settings.get("pomodoro_time", 25)))
        self.timer_entry.bind("<Return>", lambda event: self.on_timer_change(self.timer_entry.get()))

    def on_theme_change(self, choice):
        self.controller.save_settings({"theme": choice})
        ctk.set_appearance_mode(choice)

    def on_timer_change(self, choice):
        try:
            minutes = int(choice)
            self.controller.save_settings({"pomodoro_time": minutes})
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the timer.")

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
