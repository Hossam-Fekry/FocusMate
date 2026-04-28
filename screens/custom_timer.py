import customtkinter as ctk
import tkinter as tk
import os
import json
from PIL import Image
from plyer import notification
import winsound
from tkinter import messagebox
import datetime
from screens.base_screen import BaseScreen

class CustomTimerScreen(BaseScreen):
    def setup_ui(self):
        self.settings_file = "data/settings.json"
        self.progress_file = "data/progress.json"
        
        self.time_running = False
        self.paused = False
        self.remaining_time = 0
        self.elapsed_seconds = 0

        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, fg_color="transparent", hover_color="#333333", command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        ctk.CTkLabel(self, text="Customized Timer", font=("Arial", 24, "bold")).pack(pady=20)

        self.time_frame = ctk.CTkFrame(self)
        self.time_frame.pack(pady=10)

        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")

        self.hours_entry = ctk.CTkEntry(self.time_frame, textvariable=self.hours_var, width=70)
        self.hours_entry.grid(row=0, column=0, padx=5)
        ctk.CTkLabel(self.time_frame, text="h").grid(row=1, column=0)

        self.minutes_entry = ctk.CTkEntry(self.time_frame, textvariable=self.minutes_var, width=70)
        self.minutes_entry.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(self.time_frame, text="m").grid(row=1, column=1)

        self.seconds_entry = ctk.CTkEntry(self.time_frame, textvariable=self.seconds_var, width=70)
        self.seconds_entry.grid(row=0, column=2, padx=5)
        ctk.CTkLabel(self.time_frame, text="s").grid(row=1, column=2)

        self.timer_label = ctk.CTkLabel(self, text="00:00:00", font=("Arial", 36, "bold"))
        self.timer_label.pack(pady=20)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(self.btn_frame, text="Start", fg_color="#02960C", hover_color="#005506", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=6)

        self.pause_button = ctk.CTkButton(self.btn_frame, text="Pause", fg_color="#83A400", hover_color="#455600", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=6)

        self.resume_button = ctk.CTkButton(self.btn_frame, text="Resume", fg_color="#1B6CA8", hover_color="#124970", command=self.resume_timer)
        self.resume_button.grid(row=0, column=2, padx=6)

        self.reset_button = ctk.CTkButton(self.btn_frame, text="Reset", fg_color="#C0392B", hover_color="#A93226", command=self.reset_timer)
        self.reset_button.grid(row=0, column=3, padx=6)

    def start_timer(self):
        if self.time_running:
            return
        
        h = self.hours_var.get().strip() or "0"
        m = self.minutes_var.get().strip() or "0"
        s = self.seconds_var.get().strip() or "0"

        if not (h.isdigit() and m.isdigit() and s.isdigit()):
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")
            return

        total = int(h)*3600 + int(m)*60 + int(s)
        if total <= 0:
            return
        if total > 14400:
            messagebox.showerror("Invalid Input", "Total time should be less than 4 hours.")
            return

        self.remaining_time = total
        self.time_running = True
        self.paused = False
        self.hours_entry.configure(state="disabled")
        self.minutes_entry.configure(state="disabled")
        self.seconds_entry.configure(state="disabled")
        self.start_button.configure(state="disabled")

        self.update_timer_loop()

    def update_timer_loop(self):
        if not self.time_running:
            return

        if not self.paused:
            self.remaining_time -= 1
            self.elapsed_seconds += 1
            
            mins, secs = divmod(self.remaining_time, 60)
            hrs, mins = divmod(mins, 60)
            self.timer_label.configure(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

            if self.elapsed_seconds % 60 == 0:
                self.save_progress(1)

            if self.remaining_time <= 0:
                self.on_complete()
                return

        self.after(1000, self.update_timer_loop)

    def on_complete(self):
        self.save_progress(self.elapsed_seconds // 60)
        winsound.Beep(1000, 1000)
        notification.notify(title='FocusMate', message='Timer Complete!', timeout=10)
        self.reset_timer()

    def pause_timer(self):
        self.paused = True

    def resume_timer(self):
        self.paused = False

    def reset_timer(self):
        self.time_running = False
        self.paused = False
        self.remaining_time = 0
        self.elapsed_seconds = 0
        self.timer_label.configure(text="00:00:00")
        self.hours_entry.configure(state="normal")
        self.minutes_entry.configure(state="normal")
        self.seconds_entry.configure(state="normal")
        self.start_button.configure(state="normal")

    def save_progress(self, minutes):
        if minutes <= 0: return
        data = {"sessions": []}
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r") as f:
                    data = json.load(f)
            except: pass
        
        today = datetime.date.today().isoformat()
        for session in data["sessions"]:
            if session.get("date") == today:
                session["minutes"] = session.get("minutes", 0) + minutes
                break
        else:
            data["sessions"].append({"date": today, "minutes": minutes})
        
        with open(self.progress_file, "w") as f:
            json.dump(data, f, indent=4)

    def go_back(self):
        if self.time_running:
             if not messagebox.askyesno("Exit", "Timer is running. Go back?"):
                 return
        self.time_running = False
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
