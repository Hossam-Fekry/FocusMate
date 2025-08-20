from customtkinter import *
import subprocess
from PIL import Image

root = CTk()
root.title("FocusMate")
root.geometry("800x600")
root.resizable(False, False)
root.iconbitmap("assets/logo.ico")
def start_app():
    root.destroy()  # Close the splash screen
    subprocess.run(["python", "screens/home.py"])

CTkLabel(root, text="FocusMate",font=("Arial", 36,"bold")).pack(pady=50)
logo_image = Image.open("assets/logo.png").resize((200, 200))
logo_photo = CTkImage(light_image=logo_image, dark_image=logo_image, size=(200, 200))
CTkLabel(root,text="" ,image=logo_photo).place(x=300, y=200)
start_button = CTkButton(root, text="Start", command=start_app, fg_color="#02960C",hover_color="#015606", text_color="white", font=("Arial", 16, "bold"),corner_radius=25)
start_button.place(x=334, y=450)
root.mainloop()