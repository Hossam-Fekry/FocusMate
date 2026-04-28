import customtkinter as ctk
import json
import os
from PIL import Image
from screens.base_screen import BaseScreen

class CounterScreen(BaseScreen):
    def setup_ui(self):
        self.data_file = "data/counted.json"
        self.back_icon = ctk.CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        
        self.number = self.load_count()

        ctk.CTkLabel(self, text="Counter Screen", font=("Arial", 24, "bold")).pack(pady=30)

        self.number_label = ctk.CTkLabel(self, text=str(self.number), font=("Arial", 48, "bold"))
        self.number_label.pack(pady=50)

        self.plus_button = ctk.CTkButton(self, text="+", command=self.plus, fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25)
        self.plus_button.place(x=25, y=160)

        self.minus_button = ctk.CTkButton(self, text="-", command=self.minus, fg_color="#C0392B", hover_color="#A93226", text_color="white", font=("Arial", 16, "bold"), corner_radius=25)
        self.minus_button.place(x=300, y=160)

        self.back_button = ctk.CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)

    def load_count(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as file:
                    count = json.load(file)
                    return count.get("count", 0)
        except:
            return 0
        return 0

    def save_count(self, data):
        with open(self.data_file, "w") as file:
            json.dump({"count": data}, file, indent=4)

    def plus(self):
        self.number += 1
        self.number_label.configure(text=str(self.number))
        self.save_count(self.number)

    def minus(self):
        self.number -= 1
        self.number_label.configure(text=str(self.number))
        self.save_count(self.number)

    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
