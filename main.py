import customtkinter as ctk
import json
import os
from utils.ui_function import center_window

# Screen Imports
from screens.home import HomeScreen
from screens.pomodoro import PomodoroScreen
from screens.todo import TodoScreen
from screens.settings import SettingsScreen
from screens.counter import CounterScreen
from screens.Ai import AiScreen
from screens.stats import StatsScreen
from screens.custom_timer import CustomTimerScreen
from screens.music import MusicScreen
from screens.translator import TranslatorScreen
from screens.video_player import VideoPlayerScreen
from screens.goals import GoalsScreen

class FocusMateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_screen = None
        self.title("FocusMate")
        self.iconbitmap("assets/logo.ico")
        
        # Load settings
        self.settings_file = "data/settings.json"
        self.settings = self.load_settings()
        ctk.set_appearance_mode(self.settings.get("theme", "dark"))
        
        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.bind("<Escape>", self.handle_escape)  # Global Escape key binding to go back to Home

        # Dictionary to store screen classes and their desired window sizes
        self.screen_configs = {
            HomeScreen: "1000x600",
            PomodoroScreen: "400x300",
            TodoScreen: "500x600",
            SettingsScreen: "400x250",
            CounterScreen: "450x350",
            AiScreen: "500x600",
            StatsScreen: "600x550",
            CustomTimerScreen: "610x380",
            MusicScreen: "400x400",
            TranslatorScreen: "750x600",
            VideoPlayerScreen: "800x650",
            GoalsScreen: "500x600"
        }

        # Initially show Home Screen
        self.show_frame(HomeScreen)

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
        return {"theme": "dark", "pomodoro_time": 25}

    def handle_escape(self, event=None):
        if self.current_screen and hasattr(self.current_screen, "go_back"):
            self.current_screen.go_back()

    def save_settings(self, new_settings):
        self.settings.update(new_settings)
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def show_frame(self, page_class):
        """Destroys the current frame and creates a new one of page_class."""
        # Update window geometry based on screen config
        if page_class in self.screen_configs:
            geo = self.screen_configs[page_class]
            width, height = map(int, geo.split('x'))
            self.geometry(geo)
            center_window(self, width, height)

        # Clear existing frame
        for child in self.container.winfo_children():
            if hasattr(child, "stop_video"): # Specific for VideoPlayerScreen
                child.stop_video()
            child.destroy()

        # Create new frame
        frame = page_class(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        self.current_screen = frame
    

if __name__ == "__main__":
    app = FocusMateApp()
    app.mainloop()
