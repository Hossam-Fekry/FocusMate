from customtkinter import *
from PIL import Image

def go_back():
    print("رجوع للشاشة السابقة")

root = CTk()
root.geometry("500x400")

# تحميل أيقونة السهم (لازم يكون عندك صورة سهم مثلاً back.png)
back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))

back_button = CTkButton(
    root,
    text="رجوع",
    image=back_icon,
    compound="left",   # يحط النص جنب الأيقونة
    fg_color="transparent",  # شفاف
    hover_color="#333333",   # لون عند المرور
    text_color="white",
    font=("Arial", 16, "bold"),
    command=go_back
)
back_button.place(x=10, y=10)  # مكان الزر أعلى يسار

root.mainloop()

