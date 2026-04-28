import customtkinter as ctk
import os
import requests
from PIL import Image
from langdetect import detect
from tkinter import messagebox
from screens.base_screen import BaseScreen

class TranslatorScreen(BaseScreen):
    def setup_ui(self):
        self.translated_texts = {}
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        self.right_arrow_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/right_arrow.png"), size=(35, 35))
        self.translator_image = ctk.CTkImage(dark_image=Image.open("./assets/icons/translator.png"), size=(150, 150))

        ctk.CTkLabel(self, image=self.translator_image, text="").pack(pady=30)

        self.language_menu = ctk.CTkOptionMenu(self, values=["auto", "en", "es", "fr", "de", "it", "ja", "ko", "pt", "ru", "tr", "zh", "ar"], width=200, command=lambda v: self.update_output())
        self.language_menu.place(x=70, y=210)
        self.language_menu.set("auto")

        self.target_menu = ctk.CTkOptionMenu(self, values=["en", "es", "fr", "de", "it", "ja", "ko", "pt", "ru", "tr", "zh", "ar"], width=200, command=lambda v: self.update_output())
        self.target_menu.place(x=500, y=210)
        self.target_menu.set("ar")

        self.main_frame = ctk.CTkFrame(self, fg_color="#1E1E1E")
        self.main_frame.pack(fill="x", side="bottom", pady=20)

        self.input_box = ctk.CTkTextbox(self.main_frame, width=350, height=300, fg_color="#2A2A2A")
        self.input_box.pack(side="left", padx=10, pady=10)
        self.input_box.bind("<KeyRelease>", self.on_user_typing)

        ctk.CTkLabel(self.main_frame, text="", image=self.right_arrow_icon).pack(side="left", padx=10)

        self.output_box = ctk.CTkTextbox(self.main_frame, width=350, height=300, fg_color="#2A2A2A", state="disabled")
        self.output_box.pack(side="right", padx=10, pady=10)

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, fg_color="transparent", hover_color="#333333", command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)
        
        self.typing_delay = None

    def translate_text(self, text, source, target):
        try:
            url = "https://api.mymemory.translated.net/get"
            params = {"q": text, "langpair": f"{source}|{target}"}
            result = requests.get(url, params=params).json()
            return result["responseData"]["translatedText"]
        except:
            return None

    def update_output(self):
        text = self.input_box.get("1.0", "end-1c").strip()
        if not text:
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.configure(state="disabled")
            return

        target_lang = self.target_menu.get()
        source_option = self.language_menu.get()
        source_lang = detect(text) if source_option == "auto" else source_option

        cache_key = f"{text}|{source_lang}|{target_lang}"
        if cache_key in self.translated_texts:
            translated = self.translated_texts[cache_key]
        else:
            translated = self.translate_text(text, source_lang, target_lang)
            if translated: self.translated_texts[cache_key] = translated

        if translated:
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.insert("1.0", translated)
            self.output_box.configure(state="disabled")

    def on_user_typing(self, event=None):
        if self.typing_delay: self.after_cancel(self.typing_delay)
        self.typing_delay = self.after(500, self.update_output)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
