# import os
# os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")
# import customtkinter as ctk
# import yt_dlp
# import vlc
# import threading

# ctk.set_appearance_mode("dark")

# # ---------------------------
# # VLC Setup
# # ---------------------------
# instance = vlc.Instance()
# player = instance.media_player_new()

# # ---------------------------
# # Get Video Stream
# # ---------------------------
# def get_video_stream(url):
#     ydl_opts = {
#         'format': 'best[ext=mp4]',
#         'quiet': True
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=False)
#         return info['url']

# # ---------------------------
# # Play Video

# # ---------------------------
# def play_video():
#     url = entry.get()

#     if url.strip() == "":
#         status_label.configure(text="❌ Enter URL")
#         return

#     status_label.configure(text="Loading... 🔄")

#     def load():
#         try:
#             video_url = get_video_stream(url)

#             media = instance.media_new(video_url)
#             player.set_media(media)
            

#             player.play()

#             status_label.configure(text="Playing 🔥")

#         except Exception as e:
#             status_label.configure(text="Error ❌")

#     threading.Thread(target=load).start()

# # ---------------------------
# # Controls
# # ---------------------------
# def pause_video():
#     player.pause()

# def stop_video():
#     player.stop()

# # ---------------------------
# # UI
# # ---------------------------
# app = ctk.CTk()
# app.geometry("500x300")
# app.title("FocusMate - Custom Player")

# title = ctk.CTkLabel(app, text="🎬 Custom Study Player", font=("Arial", 22))
# title.pack(pady=10)

# entry = ctk.CTkEntry(app, width=400, placeholder_text="Paste YouTube link...")
# entry.pack(pady=10)

# play_btn = ctk.CTkButton(app, text="Play", command=play_video)
# play_btn.pack(pady=5)

# pause_btn = ctk.CTkButton(app, text="Pause", command=pause_video)
# pause_btn.pack(pady=5)

# stop_btn = ctk.CTkButton(app, text="Stop", command=stop_video)
# stop_btn.pack(pady=5)

# status_label = ctk.CTkLabel(app, text="")
# status_label.pack(pady=10)

# app.mainloop()


import os
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")

import customtkinter as ctk
import yt_dlp
import vlc
import threading
import sys

ctk.set_appearance_mode("dark")

# ---------------------------
# VLC Setup
# ---------------------------
instance = vlc.Instance()
player = instance.media_player_new()

# ---------------------------
# Get Video Stream
# ---------------------------
def get_video_stream(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

# ---------------------------
# Play Video
# ---------------------------
def play_video():
    url = entry.get()

    if url.strip() == "":
        status_label.configure(text="❌ Enter URL")
        return

    status_label.configure(text="Loading... 🔄")

    def load():
        try:
            video_url = get_video_stream(url)

            media = instance.media_new(video_url)
            player.set_media(media)

            # 👇 مهم جدًا
            app.update()
            handle = video_frame.winfo_id()

            if sys.platform.startswith("win"):
                player.set_hwnd(handle)
            elif sys.platform.startswith("linux"):
                player.set_xwindow(handle)
            elif sys.platform == "darwin":
                player.set_nsobject(handle)

            player.play()

            status_label.configure(text="Playing 🔥")

        except Exception as e:
            status_label.configure(text=f"Error ❌ {e}")

    threading.Thread(target=load).start()

# ---------------------------
# Controls
# ---------------------------
def pause_video():
    player.pause()

def stop_video():
    player.stop()

# ---------------------------
# UI
# ---------------------------
app = ctk.CTk()
app.geometry("700x500")
app.title("FocusMate - Custom Player")

title = ctk.CTkLabel(app, text="🎬 Custom Study Player", font=("Arial", 22))
title.pack(pady=10)

# 🎥 Video Frame (هنا الفيديو هيظهر)
video_frame = ctk.CTkFrame(app, width=640, height=300)
video_frame.pack(pady=10)
video_frame.pack_propagate(False)

# 🔗 URL Entry
entry = ctk.CTkEntry(app, width=500, placeholder_text="Paste YouTube link...")
entry.pack(pady=10)

# 🎮 Buttons Frame
controls_frame = ctk.CTkFrame(app, fg_color="transparent")
controls_frame.pack(pady=5)

play_btn = ctk.CTkButton(controls_frame, text="Play ▶", command=play_video)
play_btn.pack(side="left", padx=10)

pause_btn = ctk.CTkButton(controls_frame, text="Pause ⏸", command=pause_video)
pause_btn.pack(side="left", padx=10)

stop_btn = ctk.CTkButton(controls_frame, text="Stop ⏹", command=stop_video)
stop_btn.pack(side="left", padx=10)

# 📊 Status
status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=10)

app.mainloop()