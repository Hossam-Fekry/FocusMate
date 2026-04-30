import customtkinter as ctk
import threading
import time

ctk.set_appearance_mode("dark")

# --------------------------
# 🧠 Global State
# --------------------------
time_left = 1500
running = False

# --------------------------
# ⏱️ Timer Logic
# --------------------------
def run_timer():
    global time_left, running
    while running and time_left > 0:
        time.sleep(1)
        time_left -= 1

def start_timer():
    global running
    if not running:
        running = True
        threading.Thread(target=run_timer, daemon=True).start()

# --------------------------
# 🪟 FLOATING WINDOW = ROOT
# --------------------------
root = ctk.CTk()
root.geometry("220x110")
root.attributes("-topmost", True)
root.overrideredirect(True)
root.attributes("-alpha", 0.95)

frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(fill="both", expand=True, padx=5, pady=5)

label = ctk.CTkLabel(frame, text="", font=("Arial", 28, "bold"))
label.pack(expand=True)

# Close button (this closes EVERYTHING)
def close_all():
    root.destroy()

close_btn = ctk.CTkButton(frame, text="✕", width=25, height=25, command=close_all)
close_btn.place(x=185, y=5)

# Dragging
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)

# --------------------------
# 🏠 MAIN SCREEN (SECONDARY)
# --------------------------
def open_main():
    main_win = ctk.CTkToplevel(root)
    main_win.geometry("300x200")
    main_win.title("Main Screen")

    start_btn = ctk.CTkButton(main_win, text="Start Timer", command=start_timer)
    start_btn.pack(pady=20)

    close_btn = ctk.CTkButton(main_win, text="Close Main Screen", command=main_win.destroy)
    close_btn.pack(pady=10)

open_main()

# --------------------------
# 🔄 Update UI
# --------------------------
def format_time(sec):
    m, s = divmod(sec, 60)
    return f"{m:02d}:{s:02d}"

def update_ui():
    label.configure(text=format_time(time_left))
    root.after(1000, update_ui)

update_ui()

root.mainloop()