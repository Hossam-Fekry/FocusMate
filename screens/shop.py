from tkinter import messagebox
import json
from customtkinter import *
from PIL import Image
from screens.base_screen import BaseScreen
class ShopScreen(BaseScreen):
    def setup_ui(self):
        
        self.settings_file = "data/settings.json"
        self.settings = self.load_settings()
        
        self.back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
        
        coins_icon = CTkImage(light_image=Image.open("assets/icons/coins.png"), dark_image=Image.open("assets/icons/coins.png"), size=(30, 30))
        
        self.coins_label = CTkLabel(self, text=f"{self.settings['coins']} coins", image=coins_icon, compound="left", font=("Arial", 16, "bold"))
        self.coins_label.place(x=860, y=25)
        
        self.controller.resizable(False, False)
        
        self.back_button = CTkButton(self, text="", image=self.back_icon, compound="left", fg_color="transparent", hover_color="#333333", text_color="white", font=("Arial", 16, "bold"), command=self.go_back, width=40, height=40)
        self.back_button.place(x=10, y=10)
        CTkLabel(self, text="Theme Shop", font=("Arial", 36, "bold")).pack(pady=30)

        #make the Themes Frames
        self.Forest_theme = CTkFrame(self, width=200, height=250, corner_radius=25, border_width=3, border_color="#1B4332")
        self.Forest_theme.pack(side="left", padx=25, pady=25)
        self.Forest_theme_label = CTkLabel(self.Forest_theme, text="Forest Theme", font=("Arial", 16, "bold"), text_color="#000000")
        self.Forest_theme_label.pack(pady=17)
        self.Forest_theme_price_label = CTkLabel(self.Forest_theme, text="Price: 30 coins", font=("Arial", 14), text_color="#000000")
        self.Forest_theme_price_label.pack(pady=10)
        self.Forest_theme_buy_button = CTkButton(self.Forest_theme, text=f"{self.get_theme_status('forest_theme')}", fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25,command=lambda: self.proccess_Theme("forest_theme", 30))
        self.Forest_theme_buy_button.pack(pady=10)
        
        self.Coffee_theme = CTkFrame(self, width=200, height=250, corner_radius=25, border_width=3, border_color="#3C2A21")
        self.Coffee_theme.pack(side="left", padx=25, pady=25)
        self.Coffee_theme_label = CTkLabel(self.Coffee_theme, text="Coffee Theme", font=("Arial", 16, "bold"), text_color="#000000")
        self.Coffee_theme_label.pack(pady=17)
        self.Coffee_theme_price_label = CTkLabel(self.Coffee_theme, text="Price: 50 coins", font=("Arial", 14), text_color="#000000")
        self.Coffee_theme_price_label.pack(pady=10)
        self.Coffee_theme_buy_button = CTkButton(self.Coffee_theme, text=f"{self.get_theme_status('coffee_theme')}", fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25,command=lambda: self.proccess_Theme("coffee_theme", 50))
        self.Coffee_theme_buy_button.pack(pady=10)

        self.Ocean_theme = CTkFrame(self, width=200, height=250, corner_radius=25, border_width=3, border_color="#0A2647")
        self.Ocean_theme.pack(side="left", padx=25, pady=25)
        self.Ocean_theme_label = CTkLabel(self.Ocean_theme, text="Ocean Theme", font=("Arial", 16, "bold"), text_color="#000000")
        self.Ocean_theme_label.pack(pady=17)
        self.Ocean_theme_price_label = CTkLabel(self.Ocean_theme, text="Price: 15 coins", font=("Arial", 14), text_color="#000000")
        self.Ocean_theme_price_label.pack(pady=10)
        self.Ocean_theme_buy_button = CTkButton(self.Ocean_theme, text=f"{self.get_theme_status('ocean_theme')}", fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25,command=lambda: self.proccess_Theme("ocean_theme", 15))
        self.Ocean_theme_buy_button.pack(pady=10)

        self.Golden_theme = CTkFrame(self, width=200, height=250, corner_radius=25, border_width=3, border_color="#9D9200")
        self.Golden_theme.pack(side="left", padx=25, pady=25)
        self.Golden_theme_label = CTkLabel(self.Golden_theme, text="Golden Theme", font=("Arial", 16, "bold"), text_color="#000000")
        self.Golden_theme_label.pack(pady=17)
        self.Golden_theme_price_label = CTkLabel(self.Golden_theme, text="Price: 80 coins", font=("Arial", 14), text_color="#000000")
        self.Golden_theme_price_label.pack(pady=10)
        self.Golden_theme_buy_button = CTkButton(self.Golden_theme, text=f"{self.get_theme_status('golden_theme')}", fg_color="#02960C", hover_color="#015606", text_color="white", font=("Arial", 16, "bold"), corner_radius=25,command=lambda: self.proccess_Theme("golden_theme", 80))
        self.Golden_theme_buy_button.pack(pady=10)

        self.Forest_theme.pack_propagate(False)
        self.Coffee_theme.pack_propagate(False)
        self.Ocean_theme.pack_propagate(False)
        self.Golden_theme.pack_propagate(False)


    
    
    def load_settings(self):
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"coins": 0}


    def go_back(self):
        from screens.home import HomeScreen
        self.controller.show_frame(HomeScreen)
    
    def get_theme_status(self, theme_name):
        # theme_name in self.settings.get("Owned_themes", [])
        self.owned_themes = self.settings.get("Owned_themes", [])
        self.equipped_theme = self.settings.get("Equipped_theme", "dark-blue")
        if theme_name in self.owned_themes:
            if theme_name == self.equipped_theme:
                return "Equipped"
            return "Equip"
        return "Buy"
    

    def proccess_Theme(self, theme_name, price):
        if theme_name in self.settings.get("Owned_themes", []):
            # Equip the theme
            self.controller.save_settings({"Equipped_theme": theme_name})
            self.settings = self.load_settings()
            # self.update_buttons()
            self.controller.reload_theme()
            self.Forest_theme_buy_button.configure(text=self.get_theme_status("forest_theme"))
            self.Coffee_theme_buy_button.configure(text=self.get_theme_status("coffee_theme"))
            self.Ocean_theme_buy_button.configure(text=self.get_theme_status("ocean_theme"))
            self.Golden_theme_buy_button.configure(text=self.get_theme_status("golden_theme"))
        else:
            # Try to buy the theme
            coins = self.settings.get("coins", 0)
            if coins >= price:
                self.complete_payment = messagebox.askyesno("Complete Payment check",f"Do you want to spend {price} for this theme, After this payment your coins will go from {coins} to {coins - price}")
                if self.complete_payment:
                    coins -= price
                    owned_themes = self.settings.get("Owned_themes", [])
                    owned_themes.append(theme_name)
                    self.controller.save_settings({"coins": coins, "Owned_themes": owned_themes})
                    self.settings = self.load_settings()
                    self.controller.reload_theme()
                    self.coins_label.configure(text=f"{coins} coins")
                    self.Forest_theme_buy_button.configure(text=self.get_theme_status("forest_theme"))
                    self.Coffee_theme_buy_button.configure(text=self.get_theme_status("coffee_theme"))
                    self.Ocean_theme_buy_button.configure(text=self.get_theme_status("ocean_theme"))
                    self.Golden_theme_buy_button.configure(text=self.get_theme_status("golden_theme"))
                    self.settings = self.load_settings()
            else:
                messagebox.showerror("No Enough Coins", "You don't have enough coins to buy this theme Try to Study Harder.")
