import customtkinter as ctk
import os
import sys
import vlc
import threading
import yt_dlp
from PIL import Image
from tkinter import messagebox
from screens.base_screen import BaseScreen

# Ensure VLC DLLs are found
if sys.platform.startswith("win"):
    vlc_path = r"C:\Program Files\VideoLAN\VLC"
    if os.path.exists(vlc_path):
        os.add_dll_directory(vlc_path)

class VideoPlayerScreen(BaseScreen):
    def setup_ui(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.is_paused = False

        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

        ctk.CTkLabel(self, text="Media Player (Study mode)", font=("Arial", 25, "bold")).pack(pady=30)

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10)

        self.video_link_entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="Enter YouTube URL here...")
        self.video_link_entry.pack(side="left", padx=10)
        self.video_link_entry.bind("<Return>", lambda e: self.play_video())

        self.start_button = ctk.CTkButton(input_frame, text="Start video", command=self.play_video)
        self.start_button.pack(side="left", padx=10)

        self.video_frame = ctk.CTkFrame(self, width=640, height=380)
        self.video_frame.pack(pady=10, fill="x")
        self.video_frame.pack_propagate(False)

        control_frame = ctk.CTkFrame(self, height=50)
        control_frame.pack(side="bottom", pady=20)

        self.pause_button = ctk.CTkButton(control_frame, text="Pause/Resume", command=self.toggle_pause, fg_color="#5555FF", hover_color="#7777FF")
        self.pause_button.pack(side="left", padx=20)

        self.stop_button = ctk.CTkButton(control_frame, text="Stop", command=self.stop_video, fg_color="#FF5555", hover_color="#FF7777")
        self.stop_button.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=5)

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, fg_color="transparent", hover_color="#333333", command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

    def get_video_stream(self, url):
        ydl_opts = {'format': 'best[ext=mp4]', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']

    def play_video(self):
        url = self.video_link_entry.get().strip()
        if not url: return

        self.status_label.configure(text="Loading... 🔄")
        
        def load():
            try:
                stream_url = self.get_video_stream(url)
                media = self.instance.media_new(stream_url)
                self.player.set_media(media)
                
                handle = self.video_frame.winfo_id()
                if sys.platform.startswith("win"):
                    self.player.set_hwnd(handle)
                elif sys.platform.startswith("linux"):
                    self.player.set_xwindow(handle)

                self.player.play()
                self.after(0, lambda: self.status_label.configure(text="Playing 🔥"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=load, daemon=True).start()

    def toggle_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.status_label.configure(text="Paused ⏸️")
        else:
            self.player.play()
            self.status_label.configure(text="Playing 🔥")

    def stop_video(self):
        self.player.stop()
        self.status_label.configure(text="Stopped")

    def go_back(self):
        self.stop_video()
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
