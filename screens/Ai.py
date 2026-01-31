# ================== Imports ==================
from urllib import response
from customtkinter import *
import json
import os
import sys
import threading
from tkinter import messagebox
from openai import OpenAI
import datetime
from PIL import Image
import subprocess
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"sessions": []}
    else:
        return {"sessions": []}

def save_progress(minutes):
    data = load_progress()
    today = datetime.date.today().isoformat()

    # Find today's session
    for session in data["sessions"]:
        if session["date"] == today:
            session["minutes"] += minutes
            break
    else:
        data["sessions"].append({"date": today, "minutes": minutes})

    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)




# ================== Constants ==================
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "chat_history.json")
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")
PROGRESS_FILE =  os.path.join(os.path.dirname(__file__), "..", "data", "progress.json")
TASKS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")
tasks = load_tasks()
progress = load_progress()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

system_prompt =  {
    "role": "system",
    "content": f"""Your name is FocusMate an I assistant designed to help users improve their focus and productivity. You provide tips, techniques, and motivation to help users stay on track with their tasks. Always respond in a friendly and supportive manner, encouraging users to maintain their focus and achieve their goals, always answer in one sentence and do not use markdown formatting. the user has the  following tasks:{tasks} and this is his/her progress so far:{progress}"""
}


# ================== State ==================
chat_history = []
ai_running = False


# ================== Data Functions ==================
def load_settings():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_chat_history():
    global chat_history
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            chat_history = json.load(f)
    else:
        chat_history = []


def save_chat_history():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"sessions": []}
    else:
        return {"sessions": []}



# ================== AI Logic ==================
def get_ai_reply(user_message):
    #load the entire chat history including the new user message
    message = [system_prompt] + chat_history[-20:] 
    response = client.responses.create(
              input=message,
              model="openai/gpt-oss-20b",
    )
    return response.output_text


# ================== UI Helpers ==================
import re

def insert_markdown(text, role_tag):
    chat_box.configure(state="normal")

    patterns = [
        (r"\*\*(.*?)\*\*", "bold"),   # **bold**
        (r"\*(.*?)\*", "italic"),     # *italic*
        (r"`(.*?)`", "code")          # `code`
    ]

    pos = 0
    while pos < len(text):
        match = None
        tag = None

        for pattern, t in patterns:
            m = re.search(pattern, text[pos:])
            if m and (match is None or m.start() < match.start()):
                match = m
                tag = t

        if not match:
            chat_box.insert("end", text[pos:], role_tag)
            break

        start = pos + match.start()
        end = pos + match.end()

        chat_box.insert("end", text[pos:start], role_tag)
        chat_box.insert("end", match.group(1), (tag, role_tag))

        pos = end

    chat_box.insert("end", "\n")
    chat_box.configure(state="disabled")
    chat_box.see("end")


def add_message(role, message):
    chat_box.configure(state="normal")

    if role == "user":
        chat_box.insert("end", "\n User: ", "user")
        chat_box.configure(state="disabled")
        insert_markdown(message, "user")
    else:
        chat_box.insert("end", "\n FocusMate: ", "ai")
        chat_box.configure(state="disabled")
        insert_markdown(message, "ai")



# ================== Actions ==================
def send_message(event=None):
    user_message = input_entry.get().strip()
    if not user_message:
        return

    input_entry.delete(0, "end")

    chat_history.append({"role": "user", "content": user_message})
    add_message("user", user_message)

    threading.Thread(
        target=process_ai_reply,
        args=(user_message,),
        daemon=True
    ).start()


def process_ai_reply(user_message):
    ai_reply = get_ai_reply(user_message)

    chat_history.append({"role": "assistant", "content": ai_reply})
    save_chat_history()

    add_message("assistant", ai_reply)



# ================== Navigation ==================
def go_back(event=None):
          root.destroy()
          subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])



# ================== UI Setup ==================
root = CTk()
root.title("FocusMate - AI Assistant")
root.geometry("500x600")
root.resizable(False, False)
root.iconbitmap("assets/icons/Ai.ico")
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

center_window(root, 500, 600)

# Theme
settings = load_settings()
set_appearance_mode(settings["theme"])

# ================== Widgets ==================
title_label = CTkLabel(
    root,
    text="FocusMate AI",
    font=("Arial", 25, "bold")
)
title_label.pack(pady=10)

chat_box = CTkTextbox(
    root,
    width=460,
    height=420,
    state="disabled",
    wrap="word",
    font=("Arial", 20)

)
chat_box.tag_config("bold", foreground="#ffffff",)
chat_box.tag_config("italic", foreground="#bbbbbb")
chat_box.tag_config("code", background="#2b2b2b")
chat_box.tag_config("ai", foreground="#4CAF50")
chat_box.tag_config("user", foreground="#2196F3")


chat_box.pack(padx=10, pady=10)

input_frame = CTkFrame(root)
input_frame.pack(fill="x", padx=10, pady=10)

input_entry = CTkEntry(
    input_frame,
    placeholder_text="Ask me to help you focus..."
)
input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

send_button = CTkButton(
    input_frame,
    text="Send",
    width=80,
    command=send_message
)
send_button.pack(side="right")

back_button = CTkButton(root, text="", image=back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=go_back,width=40, height=40)

input_entry.bind("<Return>", send_message)
root.bind('<Escape>', go_back)
back_button.place(x=10, y=10)

# ================== Init ==================
load_chat_history()
# for msg in chat_history:
#     add_message(msg["role"], msg["content"])


root.mainloop()
