import customtkinter as ctk
import os
import subprocess
import pyautogui
from PIL import Image
import requests
from tkinter import messagebox
from screens.base_screen import BaseScreen

class MusicScreen(BaseScreen):
    PLAYLISTS = {
        "Holy quaran": "spotify:playlist:2Zi4QNF4bDwRmT1P6WMYiD",
        "Focus Music": "spotify:playlist:679wCT6dVMDBxrYa5NcrXL"
    }

    def setup_ui(self):
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        self.music_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/music.png"), size=(80, 80))

        ctk.CTkLabel(self, image=self.music_icon, text="").pack(pady=15)
        ctk.CTkLabel(self, text="Music Hub", font=("Arial", 24, "bold")).pack(pady=5)

        self.playlist_var = ctk.StringVar(value="Focus Music")
        self.playlist_menu = ctk.CTkOptionMenu(self, values=list(self.PLAYLISTS.keys()), variable=self.playlist_var, width=200)
        self.playlist_menu.pack(pady=10)

        ctk.CTkButton(self, text="Open Playlist", command=self.open_playlist, fg_color="#1DB954", hover_color="#14833B").pack(pady=10)

        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.pack(pady=15)

        ctk.CTkButton(controls_frame, text="⏮", width=50, command=self.previous_track).grid(row=0, column=0, padx=5)
        ctk.CTkButton(controls_frame, text="⏯", width=50, command=self.play_pause).grid(row=0, column=1, padx=5)
        ctk.CTkButton(controls_frame, text="⏭", width=50, command=self.next_track).grid(row=0, column=2, padx=5)

        volume_frame = ctk.CTkFrame(self, fg_color="transparent")
        volume_frame.pack(pady=10)

        ctk.CTkButton(volume_frame, text="🔉", width=60, command=self.volume_down).grid(row=0, column=0, padx=10)
        ctk.CTkButton(volume_frame, text="🔊", width=60, command=self.volume_up).grid(row=0, column=1, padx=10)

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

    def open_playlist(self):
        uri = self.PLAYLISTS.get(self.playlist_var.get())
        if uri:
            subprocess.Popen(["cmd", "/c", f"start {uri}"], shell=True)

    def play_pause(self): pyautogui.press("playpause")
    def next_track(self): pyautogui.press("nexttrack")
    def previous_track(self): pyautogui.press("prevtrack")
    def volume_up(self): pyautogui.press("volumeup")
    def volume_down(self): pyautogui.press("volumedown")

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
