import customtkinter as ctk
from PIL import Image
import time
from screens.base_screen import BaseScreen
import requests
from tkinter import messagebox
class HomeScreen(BaseScreen):
    def setup_ui(self):
        # Configure layout
        self.grid_columnconfigure(0, weight=1)
        self.controller.resizable(False, False)
        
        ctk.CTkLabel(self, text="FocusMate", font=("Arial", 36, "bold")).pack(pady=50)
        self.clock_label = ctk.CTkLabel(self, text="", font=("DS-Digital", 50, "bold"))
        self.clock_label.pack(pady=100)

        self.time_update()

        # Load Icons from file system
        icons = {
            "counter": "assets/icons/counter.png",
            "custom-timer": "assets/icons/custom-timer.png",
            "pomodoro": "assets/icons/pomodoro-timer.png",
            "Video-Player": "assets/icons/video-player.png",
            "todo-list": "assets/icons/todo-list.png",
            "statics": "assets/icons/statics.png",
            "translator": "assets/icons/translator.png",
            "music": "assets/icons/music.png",
            "Ai": "assets/icons/Ai.png",
            "settings": "assets/icons/settings.png",
        }

        self.navbar_frame = ctk.CTkFrame(self, height=60, fg_color="#1E1E1E")
        
        # Mapping names to classes (I'll need to import them or use strings)
        # For now, I'll use a dynamic approach or just strings that the controller can handle
        
        for i, (name, path) in enumerate(icons.items()):
            try:
                ico = ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(40, 40))
                button = ctk.CTkButton(
                    self.navbar_frame, 
                    text="", 
                    image=ico, 
                    width=50, 
                    height=50,
                    fg_color="transparent",
                    hover_color="#333333", 
                    command=lambda n=name: self.change_screen(n)
                )
                button.grid(row=0, column=i, padx=15, pady=5)
            except Exception as e:
                print(f"Error loading icon {path}: {e}")

        self.navbar_frame.pack(anchor="center", side="bottom", pady=20)

    def time_update(self):
        current_time = time.strftime("%I:%M:%S %p")
        self.clock_label.configure(text=current_time)
        self.after(1000, self.time_update)
    def is_connected(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except requests.ConnectionError:
            return False
        except requests.ReadTimeout or requests.ConnectTimeout:
            return False

    def change_screen(self, screen_name):
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

        mapping = {
            "pomodoro": PomodoroScreen,
            "todo-list": TodoScreen,
            "settings": SettingsScreen,
            "counter": CounterScreen,
            "Ai": AiScreen,
            "statics": StatsScreen,
            "custom-timer": CustomTimerScreen,
            "music": MusicScreen,
            "translator": TranslatorScreen,
            "Video-Player": VideoPlayerScreen,
            "Goal": GoalsScreen
        }

        if screen_name in mapping:
            if screen_name == "Ai" and not self.is_connected() or screen_name == "translator" and not self.is_connected() or screen_name == "music" and not self.is_connected() or screen_name == "Video-Player" and not self.is_connected():
                messagebox.showerror(title="No Internet Connection", message=f"Please connect to the internet to use the {screen_name} features.")
                return
            else:
                self.controller.show_frame(mapping[screen_name])

        else:
            print(f"Screen {screen_name} not implemented yet in OOP.")
