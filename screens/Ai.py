import customtkinter as ctk
import json
import os
import threading
from tkinter import messagebox
from openai import OpenAI
import datetime
from PIL import Image
from dotenv import load_dotenv
import requests
import re
from screens.base_screen import BaseScreen

load_dotenv()

class AiScreen(BaseScreen):
    def setup_ui(self):
        self.data_file = "data/chat_history.json"
        self.progress_file = "data/progress.json"
        self.tasks_file = "data/tasks.json"

        self.chat_history = []
        self.load_chat_history()

        self.tasks = self.load_tasks()
        self.progress = self.load_progress()

        # AI Client
        api_key = os.getenv("GROQ_API_KEY")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        ) if api_key else None

        self.back_icon = ctk.CTkImage(
            dark_image=Image.open("./assets/icons/back.png"),
            size=(25, 25)
        )

        # ================= UI =================
        ctk.CTkLabel(self, text="FocusMate AI", font=("Arial", 25, "bold")).pack(pady=10)

        self.chat_box = ctk.CTkTextbox(self, width=460, height=400, state="disabled", wrap="word", font=("Arial", 16))
        self.chat_box.tag_config("bold", foreground="#ffffff")
        self.chat_box.tag_config("italic", foreground="#bbbbbb")
        self.chat_box.tag_config("code", background="#2b2b2b")
        self.chat_box.tag_config("ai", foreground="#4CAF50")
        self.chat_box.tag_config("user", foreground="#2196F3")
        self.chat_box.pack(padx=10, pady=10)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask me to help you focus...")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        ctk.CTkButton(input_frame, text="Send", width=80, command=self.send_message).pack(side="right")

        ctk.CTkButton(
            self, text="", image=self.back_icon,
            fg_color="transparent", hover_color="#333333",
            command=self.go_back, width=40, height=40
        ).place(x=10, y=10)

        if not self.is_connected():
            messagebox.showerror("No Connection", "Internet required")

    # ================= Data =================
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                return json.load(open(self.tasks_file, "r", encoding="utf-8"))
            except:
                return []
        return []

    def load_progress(self):
        if os.path.exists(self.progress_file):
            try:
                return json.load(open(self.progress_file, "r", encoding="utf-8"))
            except:
                return {"sessions": []}
        return {"sessions": []}

    def save_progress(self, minutes):
        data = self.load_progress()
        today = datetime.date.today().isoformat()

        for session in data["sessions"]:
            if session["date"] == today:
                session["minutes"] += minutes
                break
        else:
            data["sessions"].append({"date": today, "minutes": minutes})

        json.dump(data, open(self.progress_file, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

    def load_chat_history(self):
        if os.path.exists(self.data_file):
            try:
                self.chat_history = json.load(open(self.data_file, "r", encoding="utf-8"))
            except:
                self.chat_history = []

    def save_chat_history(self):
        json.dump(self.chat_history, open(self.data_file, "w", encoding="utf-8"), indent=4, ensure_ascii=False)

    # ================= AI =================
    def build_system_prompt(self):
        return {
            "role": "system",
            "content": f"You are FocusMate AI, a productivity assistant, answer shortly in one sentence, tasks:{self.tasks}, progress:{self.progress}"
        }

    def get_ai_reply(self):
        messages = [self.build_system_prompt()] + self.chat_history[-20:]

        response = self.client.responses.create(
            model="openai/gpt-oss-20b",
            input=messages
        )
        return response.output_text

    # ================= Actions =================
    def send_message(self):
        msg = self.input_entry.get().strip()
        if not msg or not self.client:
            return

        self.input_entry.delete(0, "end")

        self.chat_history.append({"role": "user", "content": msg})
        self.add_message("user", msg)

        threading.Thread(target=self.process_ai_reply, daemon=True).start()

    def process_ai_reply(self):
        try:
            reply = self.get_ai_reply()

            self.chat_history.append({"role": "assistant", "content": reply})
            self.save_chat_history()

            self.after(0, lambda: self.add_message("assistant", reply))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("AI Error", str(e)))

    # ================= Markdown =================
    def insert_markdown(self, text, role_tag):
        patterns = [
            (r"\*\*(.*?)\*\*", "bold"),
            (r"\*(.*?)\*", "italic"),
            (r"`(.*?)`", "code")
        ]

        pos = 0
        while pos < len(text):
            match, tag = None, None

            for pattern, t in patterns:
                m = re.search(pattern, text[pos:])
                if m and (match is None or m.start() < match.start()):
                    match, tag = m, t

            if not match:
                self.chat_box.insert("end", text[pos:], role_tag)
                break

            start = pos + match.start()
            end = pos + match.end()

            self.chat_box.insert("end", text[pos:start], role_tag)
            self.chat_box.insert("end", match.group(1), (tag, role_tag))

            pos = end

        self.chat_box.insert("end", "\n")

    def add_message(self, role, message):
        self.chat_box.configure(state="normal")

        tag = "user" if role == "user" else "ai"
        self.chat_box.insert("end", f"\n {'User' if role=='user' else 'FocusMate'}: ", tag)

        self.insert_markdown(message, tag)

        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    # ================= Utils =================
    def is_connected(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)