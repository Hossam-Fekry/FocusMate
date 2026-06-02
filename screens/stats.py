from customtkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from PIL import Image
from screens.base_screen import BaseScreen

class StatsScreen(BaseScreen):
    def setup_ui(self):
        self.data_file = "data/progress.json"
        self.back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

        self.back_button = CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        CTkLabel(self, text="Working Time Statistics", font=("Arial", 28, "bold")).pack(pady=20)

        self.total_time_label = CTkLabel(self, text=f"Total focus time :", font=("Arial", 20, "bold"))
        self.total_time_label.pack(pady=(0, 10))
        
        self.total_Pomodoro_label = CTkLabel(self, text=f"Total Pomodoro sessions :", font=("Arial", 20, "bold"))
        self.total_Pomodoro_label.pack(pady=(0, 10))
        

        self.chart_frame = CTkFrame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        self.refresh_chart()

    def load_progress(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("sessions", [])
            except:
                return []
        return []

    def get_stats_by_date(self, sessions):
        stats = {}
        for session in sessions:
            date = session.get("date")
            minutes = session.get("minutes", 0)
            if date:
                stats[date] = stats.get(date, 0) + minutes
        return stats
    
    def get_total_focus_time(self, sessions):
        total_focus_time = sum(
            session["minutes"]
            for session in sessions
        )
        return total_focus_time

    def refresh_chart(self):
        sessions = self.load_progress()
        stats = self.get_stats_by_date(sessions)
        total_focus_time = self.get_total_focus_time(sessions)

        self.total_time_label.configure(text=f"Total focus time : {total_focus_time} minutes")
        self.total_Pomodoro_label.configure(text=f"Total Pomodoro sessions : {total_focus_time // 25}")
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not stats:
            CTkLabel(self.chart_frame, text="No data to display.", font=("Arial", 16)).pack(pady=20)
            return

        labels = list(stats.keys())[-7:] # Last 7 days
        sizes = [stats[l] for l in labels]

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.bar(labels, sizes, color="#02960C")
        ax.set_ylabel("Minutes")
        ax.set_title("Working Time with date", fontweight="bold", fontsize=15)
        plt.xticks(rotation=30, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
