import customtkinter as ctk
import json
import os
from utils.ui_function import center_window
import sys
import ctypes

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
from screens.shop import ShopScreen
from screens.edit_distraction_list import EditDistractionListScreen
from utils.pomodoro_manager import PomodoroSessionManager


class FocusMateApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.current_screen = None

        self.title("FocusMate")
        self.iconbitmap("assets/logo.ico")

        # Load settings
        self.settings_file = "data/settings.json"
        self.settings = self.load_settings()

        ctk.set_appearance_mode("dark")

        self.Equipped_theme = self.settings.get(
            "Equipped_theme",
            "dark-blue"
        )

        ctk.set_default_color_theme(
            f"data/{self.Equipped_theme}.json"
        )

        self.HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"

        # Distraction list file
        self.DISTRACTIONS_FILE = "data/distraction_list.json"

        self.START_MARK = "# FOCUSMATE START"
        self.END_MARK = "# FOCUSMATE END"

        # Managers
        self.pomodoro_manager = PomodoroSessionManager(self)
        self.floating_timer = None

        # Main container
        self.container = ctk.CTkFrame(self)
        self.container.pack(
            side="top",
            fill="both",
            expand=True
        )

        self.container.grid_rowconfigure(
            0,
            weight=1
        )

        self.container.grid_columnconfigure(
            0,
            weight=1
        )

        self.bind(
            "<Escape>",
            self.handle_escape
        )

        # Dictionary to store screen classes and their desired window sizes
        self.screen_configs = {
            HomeScreen: "1000x600",
            PomodoroScreen: "400x300",
            TodoScreen: "500x600",
            SettingsScreen: "400x300",
            CounterScreen: "450x350",
            AiScreen: "500x600",
            StatsScreen: "600x735",
            CustomTimerScreen: "610x380",
            MusicScreen: "400x400",
            TranslatorScreen: "750x600",
            VideoPlayerScreen: "800x650",
            ShopScreen: "1000x600",
            EditDistractionListScreen: "500x600"
        }

        # Initially show Home Screen
        self.show_frame(HomeScreen)

        # Handle window closing
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_closing
        )

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):

                with open(
                    self.settings_file,
                    "r"
                ) as f:

                    return json.load(f)

        except Exception as e:
            print(
                f"Error loading settings: {e}"
            )

        return {
            "Equipped_theme": "dark-blue",
            "pomodoro_time": 25
        }

    def handle_escape(self, event=None):

        if (
            self.current_screen
            and hasattr(
                self.current_screen,
                "go_back"
            )
        ):

            self.current_screen.go_back()

    def save_settings(self, new_settings):

        self.settings.update(new_settings)

        with open(
            self.settings_file,
            "w"
        ) as f:

            json.dump(
                self.settings,
                f,
                indent=4
            )

    def show_frame(self, page_class):

        # geometry
        if page_class in self.screen_configs:

            geo = self.screen_configs[page_class]

            width, height = map(
                int,
                geo.split('x')
            )

            self.geometry(geo)

            center_window(
                self,
                width,
                height
            )

        old_frame = self.current_screen

        new_frame = page_class(
            parent=self.container,
            controller=self
        )

        # 👇 مهم: استخدم place بدل grid
        new_frame.place(
            x=self.winfo_width(),
            y=0,
            relwidth=1,
            relheight=1
        )

        self.animate_transition(
            old_frame,
            new_frame
        )

        self.current_screen = new_frame

    def animate_transition(
        self,
        old_frame,
        new_frame
    ):

        width = self.winfo_width()

        step = 20
        delay = 10

        def slide(x):

            if x <= 0:

                new_frame.place(
                    x=0,
                    y=0,
                    relwidth=1,
                    relheight=1
                )

                if old_frame:
                    old_frame.destroy()

                return

            new_frame.place(
                x=x,
                y=0
            )

            if old_frame:

                old_frame.place(
                    x=x - width,
                    y=0
                )

            self.after(
                delay,
                lambda: slide(x - step)
            )

        slide(width)

    def reload_theme(self):

        ctk.set_default_color_theme(
            f"data/{self.settings.get('Equipped_theme', 'dark-blue')}.json"
        )

    def is_admin(self):

        return ctypes.windll.shell32.IsUserAnAdmin()

    def read_hosts(self):

        with open(
            self.HOSTS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return f.readlines()

    def write_hosts(self, lines):

        with open(
            self.HOSTS_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            f.writelines(lines)

    # ==========================================================
    # DISTRACTION LIST
    # ==========================================================

    def load_distractions(self):

        try:

            if not os.path.exists(
                self.DISTRACTIONS_FILE
            ):
                return []

            with open(
                self.DISTRACTIONS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            return data.get(
                "websites",
                []
            )

        except Exception as e:

            print(
                f"Error loading distraction list: {e}"
            )

            return []

    def get_blocked_sites(self):

        websites = self.load_distractions()

        blocked_sites = []

        for website in websites:

            # Only block enabled websites
            if not website.get(
                "enabled",
                True
            ):
                continue

            url = website.get(
                "url",
                ""
            ).strip().lower()

            if not url:
                continue

            # Remove protocol
            url = url.replace(
                "https://",
                ""
            )

            url = url.replace(
                "http://",
                ""
            )

            # Remove trailing slash
            url = url.rstrip("/")

            # Remove www. if the user entered it
            if url.startswith("www."):

                url = url[4:]

            # Add both versions
            blocked_sites.append(
                f"127.0.0.1 {url}"
            )

            blocked_sites.append(
                f"127.0.0.1 www.{url}"
            )

        return blocked_sites

    # ==========================================================
    # BLOCKING
    # ==========================================================

    def block_sites(self):

        lines = self.read_hosts()

        # Remove old FocusMate block if it exists
        new_lines = []

        inside_block = False

        for line in lines:

            if self.START_MARK in line:

                inside_block = True
                continue

            if self.END_MARK in line:

                inside_block = False
                continue

            if not inside_block:

                new_lines.append(line)

        # Get enabled websites
        blocked_sites = self.get_blocked_sites()

        # Add new FocusMate block
        new_lines.append(
            "\n" + self.START_MARK + "\n"
        )

        for site in blocked_sites:

            new_lines.append(
                site + "\n"
            )

        new_lines.append(
            self.END_MARK + "\n"
        )

        self.write_hosts(
            new_lines
        )

    def unblock_sites(self):

        lines = self.read_hosts()

        new_lines = []

        inside_block = False

        for line in lines:

            if self.START_MARK in line:

                inside_block = True
                continue

            if self.END_MARK in line:

                inside_block = False
                continue

            if not inside_block:

                new_lines.append(line)

        self.write_hosts(
            new_lines
        )

    # ==========================================================
    # FLOATING TIMER
    # ==========================================================

    def show_floating_timer(self):

        if (
            self.floating_timer is None
            or not self.floating_timer.winfo_exists()
        ):

            from screens.floating_timer import FloatingTimer

            self.floating_timer = FloatingTimer(
                self,
                self.pomodoro_manager
            )

        else:

            self.floating_timer.lift()

            self.floating_timer.focus_force()

    # ==========================================================
    # APPLICATION CLOSE
    # ==========================================================

    def on_closing(self):

        if self.pomodoro_manager.is_running:

            self.unblock_sites()

        self.destroy()

    # ==========================================================
    # ADMIN
    # ==========================================================

    def run_as_admin(self):

        """Relaunch the script with admin privileges."""

        script = sys.argv[0]

        params = " ".join(
            sys.argv[1:]
        )

        # ShellExecute with "runas" triggers UAC popup
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            f'"{script}" {params}',
            None,
            1
        )


if __name__ == "__main__":

    app = FocusMateApp()

    app.mainloop()