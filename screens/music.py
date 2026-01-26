from customtkinter import *
import os, sys
import subprocess
import pyautogui
import PIL.Image as Image

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

# -------------------- PLAYLISTS --------------------

PLAYLISTS = {
    "Holy quaran": "spotify:playlist:2Zi4QNF4bDwRmT1P6WMYiD",
    "Focus Music": "spotify:playlist:679wCT6dVMDBxrYa5NcrXL"
}

# -------------------- SPOTIFY CONTROL --------------------

def open_playlist(choice):
    uri = PLAYLISTS.get(choice)
    if uri:
        subprocess.Popen(
            ["cmd", "/c", f"start {uri}"],
            shell=True
        )

def play_pause():
    pyautogui.press("playpause")

def next_track():
    pyautogui.press("nexttrack")

def previous_track():
    pyautogui.press("prevtrack")

def volume_up():
    pyautogui.press("volumeup")

def volume_down():
    pyautogui.press("volumedown")

# -------------------- NAVIGATION --------------------

def go_back():
    root.destroy()
    subprocess.run([
        "python",
        os.path.join(os.path.dirname(__file__), "home.py")
    ])

# -------------------- UI SETUP --------------------

root = CTk()
root.title("FocusMate - Music Hub")
root.geometry("400x350")
root.resizable(False, False)
center_window(root, 400, 350)
set_appearance_mode("dark")

root.iconbitmap("assets/icons/music.ico")

music_icon = CTkImage(
    dark_image=Image.open("./assets/icons/music.png"),
    size=(80, 80)
)

CTkLabel(root, image=music_icon, text="").pack(pady=15)

CTkLabel(
    root,
    text="Music Hub",
    font=("Arial", 24, "bold")
).pack(pady=5)

# -------------------- PLAYLIST DROPDOWN --------------------

playlist_var = StringVar(value="Focus Music")

playlist_menu = CTkOptionMenu(
    root,
    values=list(PLAYLISTS.keys()),
    variable=playlist_var,
    width=200
)
playlist_menu.pack(pady=10)

CTkButton(
    root,
    text="Open Playlist",
    command=lambda: open_playlist(playlist_var.get()),
    fg_color="#1DB954",
    hover_color="#14833B"
).pack(pady=10)

# -------------------- CONTROLS --------------------

controls_frame = CTkFrame(root, fg_color="transparent")
controls_frame.pack(pady=15)

CTkButton(controls_frame, text="⏮", width=50, command=previous_track).grid(row=0, column=0, padx=5)
CTkButton(controls_frame, text="⏯", width=50, command=play_pause).grid(row=0, column=1, padx=5)
CTkButton(controls_frame, text="⏭", width=50, command=next_track).grid(row=0, column=2, padx=5)

volume_frame = CTkFrame(root, fg_color="transparent")
volume_frame.pack(pady=10)

CTkButton(volume_frame, text="🔉", width=60, command=volume_down).grid(row=0, column=0, padx=10)
CTkButton(volume_frame, text="🔊", width=60, command=volume_up).grid(row=0, column=1, padx=10)

# -------------------- BACK BUTTON --------------------

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)

root.mainloop()
