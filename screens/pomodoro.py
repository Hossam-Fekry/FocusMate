import customtkinter as ctk
import json
import os
import sys
from PIL import Image
from tkinter import messagebox
from screens.base_screen import BaseScreen


class PomodoroScreen(BaseScreen):

    def setup_ui(self):
        self.manager = self.controller.pomodoro_manager

        # UI
        back_icon = ctk.CTkImage(
            dark_image=Image.open("./assets/icons/back.png"),
            size=(25, 25)
        )

        pomodoro_image = ctk.CTkImage(
            dark_image=Image.open("./assets/icons/pomodoro-timer.png"),
            size=(100, 100)
        )

        ctk.CTkLabel(self, image=pomodoro_image, text="").pack(pady=20)

        self.timer_label = ctk.CTkLabel(
            self,
            text=self.manager.format_time(self.manager.time_left),
            font=("Arial", 40, "bold")
        )
        self.timer_label.pack(pady=20)

        self.start_button = ctk.CTkButton(
            self, text="Start",
            fg_color="#02960C",
            command=self.start_timer,
            corner_radius=25,
            width=80,
        )
        self.start_button.place(x=50, y=240)

        self.pause_button = ctk.CTkButton(
            self, text="Pause",
            fg_color="#83A400",
            command=self.pause_timer,
            corner_radius=25,
            width=80,
        )
        self.pause_button.place(x=150, y=240)

        self.reset_button = ctk.CTkButton(
            self, text="Reset",
            fg_color="#C0392B",
            width=80,
            corner_radius=25,
            command=self.reset_timer
        )
        self.reset_button.place(x=250, y=240)

        self.back_button = ctk.CTkButton(
            self,
            text="",
            image=back_icon,
            fg_color="transparent",
            command=self.go_back,
            width=40,
            height=40
        )
        self.back_button.place(x=10, y=10)
        
        self.update_ui_loop()

    def update_ui_loop(self):
        if not self.winfo_exists():
            return
            
        self.timer_label.configure(text=self.manager.format_time(self.manager.time_left))
        
        if self.manager.is_paused:
            self.pause_button.configure(text="Resume")
        else:
            self.pause_button.configure(text="Pause")
            
        self.after(500, self.update_ui_loop)

    def start_timer(self):
        self.manager.start()

    def pause_timer(self):
        self.manager.pause()

    def reset_timer(self):
        self.manager.reset()

    def go_back(self):
        if self.manager.is_running:
            choice = messagebox.askyesnocancel(
                "Timer Running",
                "Timer is running.\n\nYes → Keep running\nNo → Stop timer\nCancel → Stay"
            )

            if choice is None:
                return

            elif choice:  # YES → keep running + open floating
                self.controller.show_floating_timer()
            else:  # NO → stop timer
                self.manager.reset()

        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
