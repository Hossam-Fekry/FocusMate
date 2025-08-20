import customtkinter as ctk
from PIL import Image

# إعداد النافذة
app = ctk.CTk()
app.geometry("800x600")
app.title("FocusMate")
ctk.set_appearance_mode("dark")

# ========== شاشة رئيسية ==========
main_frame = ctk.CTkFrame(app, fg_color="transparent")
main_frame.pack(fill="both", expand=True)

title = ctk.CTkLabel(main_frame, text="Focus Mate", font=("Arial", 24, "bold"))
title.pack(pady=20)

# هنا هتتغير حسب الشاشة
content_label = ctk.CTkLabel(main_frame, text="🏠 Home Screen", font=("Arial", 16))
content_label.pack(pady=20)

# ========== دالة لتغيير الشاشة ==========
def change_screen(screen_name):
    content_label.configure(text=f"📌 {screen_name} Screen")

# ========== Navigation Bar ==========
nav_frame = ctk.CTkFrame(app, height=60, fg_color="#1E1E1E")
nav_frame.pack(side="bottom", fill="x")

# تحميل صور الأزرار
icons = {
    "Pomodoro": "assets/icons/pomodoro-timer.png",
    "Todo": "assets/icons/todo-list.png",
    "Goals": "assets/icons/Goal.png",
    "Stats": "assets/icons/statics.png",
    "Settings": "assets/icons/settings.png"
}

for i, (name, path) in enumerate(icons.items()):
    img = ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=(40, 40))
    btn = ctk.CTkButton(nav_frame, text="", image=img, width=50, height=50,
                        fg_color="transparent", hover_color="#333333",
                        command=lambda n=name: change_screen(n))
    btn.grid(row=0, column=i, padx=15, pady=5)

app.mainloop()
