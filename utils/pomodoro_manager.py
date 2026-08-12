import threading
import time
import json
import os
import datetime
from plyer import notification
import winsound

class PomodoroSessionManager:
    def __init__(self, controller):
        self.controller = controller
        self.settings_file = "data/settings.json"
        self.data_file = "data/progress.json"
        
        # 🧠 State
        self.time_left = self.load_initial_time() * 60
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        
        self._stop_event = threading.Event()
        self._timer_thread = None

    def load_initial_time(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as file:
                    settings = json.load(file)
                    return settings.get("pomodoro_time", 25)
        except Exception as e:
            print(f"Error loading initial time: {e}")
        return 25

    def reload_settings(self):
        """Reload timer-related settings from settings.json."""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)

            if not self.is_running:
                self.time_left = settings.get("pomodoro_time", 25) * 60

        except Exception as e:
            print(f"Error reloading settings: {e}")
    
    def format_time(self, seconds):
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02d}:{secs:02d}"

    def start(self):
        if not self.is_running:
            if not self.controller.is_admin():
                self.controller.run_as_admin()
                import sys
                sys.exit()
                return
            
            self.controller.block_sites()
            self.is_running = True
            self.is_paused = False
            self._stop_event.clear()
            self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
            self._timer_thread.start()

    def pause(self):
        if self.is_running:
            self.is_paused = not self.is_paused

    def reset(self):
        self.is_running = False
        self.is_paused = False
        self._stop_event.set()
        self.time_left = self.load_initial_time() * 60
        self.elapsed_seconds = 0
        self.controller.unblock_sites()

    def _run_timer(self):
        while self.is_running and self.time_left > 0:
            if self._stop_event.is_set():
                break
            
            if not self.is_paused:
                time.sleep(1)
                self.time_left -= 1
                self.elapsed_seconds += 1
                
                # Save every minute
                if self.elapsed_seconds >= 60:
                    self.elapsed_seconds = 0
                    self.save_progress(1)
                    self.add_coins(1)
            else:
                time.sleep(0.2)
        
        if self.time_left <= 0 and self.is_running:
            self.is_running = False
            self.on_complete()

    def on_complete(self):
        self.controller.unblock_sites()
        winsound.Beep(1000, 1000)
        notification.notify(
            title='FocusMate Timer',
            message='Your timer is complete!',
            app_icon='assets/logo.ico',
            timeout=10
        )

    def save_progress(self, minutes):
        try:
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
                data["sessions"].append({
                    "date": today,
                    "minutes": minutes
                })

            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving progress: {e}")

    def add_coins(self, amount):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            else:
                settings = {"coins": 0}
            
            settings["coins"] = settings.get("coins", 0) + amount
            
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            
            # Sync back to controller settings if needed
            if hasattr(self.controller, 'settings'):
                self.controller.settings["coins"] = settings["coins"]
        except Exception as e:
            print(f"Error adding coins: {e}")
