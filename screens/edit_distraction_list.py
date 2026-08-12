import re
from screens.base_screen import BaseScreen
from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import json
import os


class EditDistractionListScreen(BaseScreen):

    def setup_ui(self):
        self.distractions_file = "data/distraction_list.json"

        # Icons
        self.delete_icon = ctk.CTkImage(
            dark_image=Image.open("assets/icons/delete.png"),
            size=(20, 20)
        )

        self.back_icon = ctk.CTkImage(
            dark_image=Image.open("./assets/icons/back.png"),
            size=(25, 25)
        )

        # Load websites
        self.websites = self.load_websites()

        # -------------------------
        # Back button
        # -------------------------

        self.back_button = ctk.CTkButton(
            self,
            text="",
            image=self.back_icon,
            compound="left",
            fg_color="transparent",
            hover_color="#333333",
            text_color="white",
            font=("Arial", 16, "bold"),
            command=self.go_back,
            width=40,
            height=40
        )

        self.back_button.place(x=10, y=10)

        # -------------------------
        # Title
        # -------------------------

        ctk.CTkLabel(
            self,
            text="Distraction List",
            font=("Arial", 24, "bold")
        ).pack(pady=30)

        # -------------------------
        # Add Website button
        # -------------------------

        self.add_button = ctk.CTkButton(
            self,
            text="Add Website",
            fg_color="#02960C",
            hover_color="#015606",
            text_color="white",
            font=("Arial", 16, "bold"),
            corner_radius=25,
            command=self.add_website
        )

        self.add_button.pack(pady=10)

        # -------------------------
        # Websites frame
        # -------------------------

        self.websites_frame = ctk.CTkScrollableFrame(
            self,
            height=350
        )

        self.websites_frame.pack(
            pady=10,
            padx=20,
            fill="both",
            expand=True
        )

        # Build website list
        self.load_website_widgets()

    # ==========================================================
    # JSON
    # ==========================================================

    def load_websites(self):

        if not os.path.exists(self.distractions_file):
            return []

        try:
            with open(
                self.distractions_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return data.get("websites", [])

        except Exception as e:
            print(f"Error loading distraction list: {e}")
            return []

    def save_websites(self):

        try:
            data = {
                "websites": self.websites
            }

            # Make sure data directory exists
            os.makedirs(
                os.path.dirname(self.distractions_file),
                exist_ok=True
            )

            with open(
                self.distractions_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as e:
            print(f"Error saving distraction list: {e}")

    # ==========================================================
    # BUILD WEBSITE LIST
    # ==========================================================

    def load_website_widgets(self):

        # Clear old widgets
        for widget in self.websites_frame.winfo_children():
            widget.destroy()

        # Create a row for every website
        for index, website in enumerate(self.websites):

            self.create_website_row(
                index,
                website
            )

    # ==========================================================
    # WEBSITE ROW
    # ==========================================================

    def create_website_row(self, index, website):

        website_row = ctk.CTkFrame(
            self.websites_frame,
            height=60,
            corner_radius=10,
            fg_color="#252525"
        )

        website_row.pack(
            fill="x",
            padx=5,
            pady=5
        )

        website_row.pack_propagate(False)

        # -------------------------
        # Website name
        # -------------------------

        website_label = ctk.CTkLabel(
            website_row,
            text=website["name"],
            font=("Arial", 15, "bold"),
            anchor="w"
        )

        website_label.pack(
            side="left",
            padx=15,
            fill="y"
        )

        # -------------------------
        # Delete button
        # -------------------------

        delete_btn = ctk.CTkButton(
            website_row,
            text="",
            image=self.delete_icon,
            width=40,
            height=40,
            fg_color="#650000",
            hover_color="#400000",
            text_color="white",
            corner_radius=8,
            command=lambda i=index: self.delete_website(i)
        )

        delete_btn.pack(
            side="right",
            padx=(5, 10)
        )

        # -------------------------
        # Rounded checkbox
        # -------------------------

        toggle = RoundedToggle(
            website_row,
            value=website.get("enabled", True),
            command=lambda i=index: self.toggle_website(i)
        )

        toggle.pack(
            side="right",
            padx=5
        )

    # ==========================================================
    # TOGGLE
    # ==========================================================

    def toggle_website(self, index):

        self.websites[index]["enabled"] = not self.websites[index].get(
            "enabled",
            True
        )

        self.save_websites()

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_website(self, index):

        if 0 <= index < len(self.websites):

            self.websites.pop(index)

            self.save_websites()

            self.load_website_widgets()

    # ==========================================================
    # ADD WEBSITE
    # ==========================================================

    def is_valid_url(self, url):
    
                # Remove spaces
                url = url.strip()
    
                # Add https:// temporarily if the user didn't write it
                check_url = url
    
                if not check_url.startswith(("http://", "https://")):
                    check_url = "https://" + check_url
    
                pattern = re.compile(
                    r"^https?://"
                    r"(?:www\.)?"
                    r"[a-zA-Z0-9-]+"
                    r"(?:\.[a-zA-Z0-9-]+)+"
                    r"(?:/.*)?$"
                )
    
                return bool(pattern.match(check_url))
    

    def add_website(self):

        # Temporary simple popup
        # We can design the real Add Website window later.

        dialog = ctk.CTkToplevel(self)

        dialog.title("Add Website")
        dialog.geometry("400x300")

        dialog.transient(self)
        dialog.grab_set()

        # -------------------------
        # Name
        # -------------------------

        ctk.CTkLabel(
            dialog,
            text="Website Name",
            font=("Arial", 14, "bold")
        ).pack(
            pady=(20, 5)
        )

        name_entry = ctk.CTkEntry(
            dialog,
            width=300,
            placeholder_text="e.g. YouTube"
        )

        name_entry.pack()

        # -------------------------
        # URL
        # -------------------------

        ctk.CTkLabel(
            dialog,
            text="Website URL",
            font=("Arial", 14, "bold")
        ).pack(
            pady=(15, 5)
        )

        url_entry = ctk.CTkEntry(
            dialog,
            width=300,
            placeholder_text="e.g. youtube.com"
        )

        url_entry.pack()

        # -------------------------
        # Add
        # -------------------------


        def confirm_add():

            name = name_entry.get().strip()
            url = url_entry.get().strip()

            # -------------------------
            # Check website name
            # -------------------------

            if not name:
                print("Website name is required.")
                return

            # -------------------------
            # Check URL
            # -------------------------

            if not url:
                print("Website URL is required.")
                return

            if not self.is_valid_url(url):
                messagebox.showerror("Invalid URL", "Please Try to copy the URL again.")
                return

            # -------------------------
            # Check duplicate URL
            # -------------------------

            for website in self.websites:

                existing_url = website["url"].strip().lower().rstrip("/")
                new_url = url.lower().rstrip("/")

                # Remove protocol for comparison
                existing_url = existing_url.replace("https://", "")
                existing_url = existing_url.replace("http://", "")

                new_url = new_url.replace("https://", "")
                new_url = new_url.replace("http://", "")

                if existing_url == new_url:

                    print("This website already exists.")
                    return

            # -------------------------
            # Add website
            # -------------------------

            self.websites.append({
                "name": name,
                "url": url,
                "enabled": True
            })

            # -------------------------
            # Save
            # -------------------------

            self.save_websites()

            # -------------------------
            # Refresh UI
            # -------------------------

            self.load_website_widgets()

            # -------------------------
            # Close dialog
            # -------------------------

            dialog.destroy()

        ctk.CTkButton(
            dialog,
            text="Add Website",
            fg_color="#02960C",
            hover_color="#015606",
            command=confirm_add
        ).pack(
            pady=25
        )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def go_back(self):

        from screens.home import HomeScreen

        self.controller.show_frame(HomeScreen)


# ==============================================================
# CUSTOM ROUNDED TOGGLE
# ==============================================================

class RoundedToggle(tk.Canvas):

    def __init__(
        self,
        parent,
        value=False,
        command=None,
        width=55,
        height=30
    ):

        super().__init__(
            parent,
            width=width,
            height=height,
            bg="#252525",
            highlightthickness=0,
            bd=0
                )

        self.width = width
        self.height = height

        self.value = value
        self.command = command

        self.bind(
            "<Button-1>",
            self.toggle
        )

        self.draw()

    def draw(self):

        self.delete("all")

        # -------------------------
        # Colors
        # -------------------------

        if self.value:

            background = "#02960C"
            knob_color = "white"

        else:

            background = "#555555"
            knob_color = "#D0D0D0"

        # -------------------------
        # Rounded background
        # -------------------------

        radius = self.height // 2

        self.create_rounded_rectangle(
            1,
            1,
            self.width - 1,
            self.height - 1,
            radius,
            fill=background,
            outline=""
        )

        # -------------------------
        # Knob
        # -------------------------

        knob_size = self.height - 6

        if self.value:

            x = self.width - knob_size - 3

        else:

            x = 3

        self.create_rounded_rectangle(
            x,
            3,
            x + knob_size,
            3 + knob_size,
            knob_size // 2,
            fill=knob_color,
            outline=""
        )

    def toggle(self, event=None):

        self.value = not self.value

        self.draw()

        if self.command:
            self.command()

    def create_rounded_rectangle(
        self,
        x1,
        y1,
        x2,
        y2,
        radius,
        **kwargs
    ):

        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return self.create_polygon(
            points,
            smooth=True,
            **kwargs
        )