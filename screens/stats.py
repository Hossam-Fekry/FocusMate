import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from PIL import Image
from screens.base_screen import BaseScreen

class StatsScreen(BaseScreen):
    def setup_ui(self):
        self.data_file = "data/progress.json"
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        ctk.CTkLabel(self, text="Pomodoro Statistics", font=("Arial", 28, "bold")).pack(pady=20)

        self.chart_frame = ctk.CTkFrame(self)
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

    def refresh_chart(self):
        sessions = self.load_progress()
        stats = self.get_stats_by_date(sessions)
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not stats:
            ctk.CTkLabel(self.chart_frame, text="No data to display.", font=("Arial", 16)).pack(pady=20)
            return

        labels = list(stats.keys())[-7:] # Last 7 days
        sizes = [stats[l] for l in labels]

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.bar(labels, sizes, color="#02960C")
        ax.set_ylabel("Minutes")
        ax.set_title("Pomodoro Minutes by Date")
        plt.xticks(rotation=30, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
