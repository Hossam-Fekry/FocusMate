import customtkinter as ctk
import json
import os
from PIL import Image
import threading
import time
import datetime
from tkinter import messagebox
from plyer import notification
import winsound
from screens.base_screen import BaseScreen

class PomodoroScreen(BaseScreen):
    def setup_ui(self):
        self.settings_file = "data/settings.json"
        self.data_file = "data/progress.json"
        self.running = False
        self.paused = False
        self.elapsed_time = 0
        self.time_left = self.load_time() * 60

        # UI Setup
        back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        pomodoro_image = ctk.CTkImage(dark_image=Image.open("./assets/icons/pomodoro-timer.png"), size=(100, 100))

        ctk.CTkLabel(self, image=pomodoro_image, text="", font=("Arial", 24, "bold")).pack(pady=20)
        
        self.timer_label = ctk.CTkLabel(self, text=self.format_time(self.time_left), font=("Arial", 40, "bold"))
        self.timer_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start", fg_color="#02960C", hover_color="#005506", text_color="white", font=("Arial", 16, "bold"), corner_radius=25, width=80, command=self.start_timer)
        self.start_button.place(x=50, y=240)

        self.pause_button = ctk.CTkButton(self, text="Pause", fg_color="#83A400", hover_color="#455600", text_color="white", font=("Arial", 16, "bold"), corner_radius=25, width=80, command=self.pause_timer)
        self.pause_button.place(x=150, y=240)

        self.reset_button = ctk.CTkButton(self, text="Reset", fg_color="#C0392B", hover_color="#A93226", text_color="white", font=("Arial", 16, "bold"), corner_radius=25, width=80, command=self.reset_timer)
        self.reset_button.place(x=250, y=240)

        self.back_button = ctk.CTkButton(self, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

    def load_time(self):
        try:
            with open(self.settings_file, "r") as file:
                settings = json.load(file)
                return settings.get("pomodoro_time", 25)
        except:
            return 25

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer_label(self):
        self.timer_label.configure(text=self.format_time(self.time_left))

    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            threading.Thread(target=self.run_timer, daemon=True).start()

    def run_timer(self):
        while self.running and self.time_left > 0:
            if not self.paused:
                time.sleep(1)
                self.time_left -= 1
                self.elapsed_time += 1
                self.update_timer_label()
                if self.elapsed_time == 60:
                    self.elapsed_time = 0
                    self.save_progress(1)
            else:
                time.sleep(0.2)
        
        if self.running and self.time_left == 0:
            self.running = False
            self.on_timer_complete()

    def on_timer_complete(self):
        self.timer_label.configure(text="00:00")
        winsound.Beep(1000, 1000)
        notification.notify(
            title='FocusMate Timer',
            message='Your timer is complete!',
            app_icon='assets/logo.ico',
            timeout=10
        )

    def pause_timer(self):
        self.paused = not self.paused
        self.pause_button.configure(text="Resume" if self.paused else "Pause")

    def reset_timer(self):
        self.running = False
        self.time_left = self.load_time() * 60
        self.elapsed_time = 0
        self.update_timer_label()

    def save_progress(self, minutes):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except:
                    data = {"sessions": []}
        else:
            data = {"sessions": []}
        
        today = datetime.date.today().isoformat()
        found = False
        for session in data["sessions"]:
            if session["date"] == today:
                session["minutes"] += minutes
                found = True
                break
        if not found:
            data["sessions"].append({"date": today, "minutes": minutes})
            
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def go_back(self):
        if self.running:
            if not messagebox.askyesno("Exit Pomodoro", "Timer is running. Are you sure you want to go back?"):
                return
        self.running = False
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
