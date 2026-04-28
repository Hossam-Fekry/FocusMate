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
        
        # AI Client setup
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
             # We should handle this gracefully in the UI
             print("GROQ_API_KEY not found.")
             self.client = None
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
            )

        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

        # UI Widgets
        title_label = ctk.CTkLabel(self, text="FocusMate AI", font=("Arial", 25, "bold"))
        title_label.pack(pady=10)

        self.chat_box = ctk.CTkTextbox(self, width=460, height=400, state="disabled", wrap="word", font=("Arial", 16))
        self.chat_box.tag_config("bold", foreground="#ffffff")
        self.chat_box.tag_config("italic", foreground="#bbbbbb")
        self.chat_box.tag_config("ai", foreground="#4CAF50")
        self.chat_box.tag_config("user", foreground="#2196F3")
        self.chat_box.pack(padx=10, pady=10)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.input_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask me to help you focus...")
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(input_frame, text="Send", width=80, command=self.send_message)
        self.send_button.pack(side="right")

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

        # Initial checks
        if not self.is_connected():
            messagebox.showerror("No Connection", "Internet connection required for AI.")

    def is_connected(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except:
            return False

    def load_chat_history(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.chat_history = json.load(f)
            except:
                self.chat_history = []

    def save_chat_history(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=4, ensure_ascii=False)

    def send_message(self):
        user_message = self.input_entry.get().strip()
        if not user_message or not self.client:
            return

        self.input_entry.delete(0, "end")
        self.chat_history.append({"role": "user", "content": user_message})
        self.add_message("user", user_message)

        threading.Thread(target=self.process_ai_reply, args=(user_message,), daemon=True).start()

    def process_ai_reply(self, user_message):
        try:
            # Simple system prompt
            messages = [{"role": "system", "content": "You are FocusMate, a friendly productivity assistant. Keep replies concise."}]
            messages.extend(self.chat_history[-10:]) # last 10 messages
            
            response = self.client.chat.completions.create(
                model="llama3-8b-8192", # or another groq model
                messages=messages
            )
            ai_reply = response.choices[0].message.content
            
            self.chat_history.append({"role": "assistant", "content": ai_reply})
            self.save_chat_history()
            
            # Use after() to update UI from thread
            self.after(0, lambda: self.add_message("assistant", ai_reply))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("AI Error", str(e)))

    def add_message(self, role, message):
        self.chat_box.configure(state="normal")
        tag = "user" if role == "user" else "ai"
        self.chat_box.insert("end", f"\n {'User' if role == 'user' else 'FocusMate'}: ", tag)
        self.chat_box.insert("end", f"{message}\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
