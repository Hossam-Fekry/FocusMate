from customtkinter import * 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")
from utils.ui_function import center_window
import json
import vlc
import threading
import yt_dlp
from PIL import Image
import subprocess
from tkinter import messagebox
import requests


SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")

# * VLC SETUP
instance = vlc.Instance()
player = instance.media_player_new()
is_paused = False

# ---------------------------
#* Get Video Stream
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
# * Play Video

# ---------------------------
# def play_video():
#     url = Video_link_entry.get()

#     if url.strip() == "":
#         messagebox.showerror("Error", "Please enter a YouTube URL.")
#         return


#     def load():
#         try:
#             video_url = get_video_stream(url)

#             media = instance.media_new(video_url)
#             player.set_media(media)
            

#             player.play()


#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to play video: {str(e)}")

#     threading.Thread(target=load).start()

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False
    except requests.exceptions.ReadTimeout:
        return False


def is_valid_video(url):
    import yt_dlp

    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return True, info
    except Exception as e:
        return False, str(e)

def play_video(event = None):
    url = Video_link_entry.get()

    if url.strip() == "":
        messagebox.showerror("Error", "Please enter a URl to run it ...")
        status_label.configure(text="❌ Enter URL")
        return
    
    status_label.configure(text="Checking link... 🔍")
    valid, data = is_valid_video(url)
    
    if not valid:
        messagebox.showerror("Error", "Invalid or unsupported video link")
        status_label.configure(text="❌ Invalid link")
        return
    
    status_label.configure(text="Loading... 🔄")

    def load():
        try:
            video_url = get_video_stream(url)

            media = instance.media_new(video_url)
            player.set_media(media)

            
            root.update()
            handle = video_frame.winfo_id()

            if sys.platform.startswith("win"):
                player.set_hwnd(handle)
            elif sys.platform.startswith("linux"):
                player.set_xwindow(handle)
            # elif sys.platform == "darwin":
            #     player.set_nsobject(handle)

            player.play()
            Video_link_entry.delete(0, END)
            Video_link_entry.configure(state = "disabled")
            start_button.configure(state = "disabled")
            status_label.configure(text="Playing 🔥")
            title = data.get("title", "Unknown")
            status_label.configure(text=f"Playing 🎬 {title}")            


            

        except Exception as e:
            messagebox.showerror("Error", f"Something wrong happened: {e}")
            status_label.configure(text=f"Error ❌ {e}")


    threading.Thread(target=load).start()

def go_back(event = None):
    root.destroy()
    subprocess.run([sys.executable, "screens/home.py"])

# ---------------------------
#* Controls
# ---------------------------
def pause_video(event = None):
    global is_paused
    if player.is_playing():
        player.pause()
        is_paused = True
        status_label.configure(text="Paused ⏸️")
    elif is_paused:
        player.play()
        is_paused = False
        status_label.configure(text="Playing 🔥")

def stop_video():
    player.stop()
    Video_link_entry.configure(state = "normal")
    start_button.configure(state = "normal")

def load_theme():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["theme"]
    

# ! make the go back function

#######################################   

root = CTk()
root.title("Media player")
root.geometry("800x600")
root.resizable(False, False)
center_window(root, 800, 600)
root.iconbitmap("assets/icons/video-player.ico")
set_appearance_mode(load_theme())
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

CTkLabel(root, text="Media Player (Study mode)", font=("Arial", 25, "bold")).pack(pady=30)
# Video_entry = CTkEntry(root, width=400, placeholder_text="Enter YouTube URL here...").pack( padx = 10,side = LEFT)
# Start_button = CTkButton(root,text = "Start video").pack(side = LEFT,  padx = 10)

input_frame = CTkFrame(root, fg_color="transparent")
input_frame.pack(pady=10)

Video_link_entry = CTkEntry(input_frame, width=400, placeholder_text="Enter YouTube URL here...")
Video_link_entry.pack(side=LEFT, padx=10)

start_button = CTkButton(input_frame, text="Start video", command=play_video)
start_button.pack(side=LEFT, padx=10)


video_frame = CTkFrame(root, width=640, height=380)
video_frame.pack(pady=10,fill = X)
video_frame.pack_propagate(False)

control_frame = CTkFrame(root, height=50)
control_frame.pack(side = BOTTOM)

Pause_button = CTkButton(control_frame, text="Pause video", command=pause_video, fg_color="#5555FF", hover_color="#7777FF")
Pause_button.pack(side = LEFT, pady=10, padx = 20)
status_label = CTkLabel(control_frame, text="")
status_label.pack(side = LEFT, padx = 20)
Stop_button = CTkButton(control_frame, text="Stop video", command=stop_video, fg_color="#FF5555", hover_color="#FF7777")
Stop_button.pack(pady=10, side = LEFT, padx = 20)


back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)
back_button.place(x=10, y=10)

root.bind("<Escape>", go_back)
root.bind("<space>", pause_video)
Video_link_entry.bind("<Return>", play_video)

if is_connected():
    root.mainloop()
else:
    messagebox.showerror("Bad internet connection", "No internet connection. Please connect to the internet or try to have a stable connection to use the translator.")

