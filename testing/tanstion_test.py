import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("800x500")
app.title("Transition Test")

# ---------------------------
# Frames
# ---------------------------
setup_frame = ctk.CTkFrame(app)
study_frame = ctk.CTkFrame(app)

setup_frame.place(relwidth=1, relheight=1)
study_frame.place(relwidth=1, relheight=1)

# ---------------------------
# Setup Screen
# ---------------------------
setup_label = ctk.CTkLabel(setup_frame, text="Setup Screen", font=("Arial", 30))
setup_label.pack(pady=50)

start_btn = ctk.CTkButton(setup_frame, text="Start ▶️")
start_btn.pack()

# ---------------------------
# Study Screen
# ---------------------------
study_label = ctk.CTkLabel(study_frame, text="Study Mode 🎥", font=("Arial", 30))
study_label.pack(pady=50)

back_btn = ctk.CTkButton(study_frame, text="⬅ Back")
back_btn.pack()

# ---------------------------
# Animations
# ---------------------------

def fade_out(callback, alpha=1.0):
    if alpha > 0:
        alpha -= 0.05
        app.attributes("-alpha", alpha)
        app.after(15, lambda: fade_out(callback, alpha))
    else:
        callback()

def fade_in(alpha=0.0):
    if alpha < 1:
        alpha += 0.05
        app.attributes("-alpha", alpha)
        app.after(15, lambda: fade_in(alpha))

def switch_to_study():
    setup_frame.lower()
    study_frame.lift()
    fade_in()

def switch_to_setup():
    study_frame.lower()
    setup_frame.lift()
    fade_in()

# ---------------------------
# Button Actions
# ---------------------------
start_btn.configure(command=lambda: fade_out(switch_to_study))
back_btn.configure(command=lambda: fade_out(switch_to_setup))

# ---------------------------
# Start State
# ---------------------------
study_frame.lower()

app.mainloop()