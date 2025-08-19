import tkinter as tk
import customtkinter as ctk
import time
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Customized Timer")
root.geometry("400x400")

# --- Variables ---
hours_var = tk.StringVar(value="0")
minutes_var = tk.StringVar(value="0")
seconds_var = tk.StringVar(value="0")
time_running = False
paused = False
remaining_time = 0

# --- Functions ---
def start_timer():
    global time_running, remaining_time, paused
    if time_running:
        return
    paused = False
    h = int(hours_var.get())
    m = int(minutes_var.get())
    s = int(seconds_var.get())
    remaining_time = h*3600 + m*60 + s
    if remaining_time <= 0:
        return
    time_running = True
    threading.Thread(target=run_timer, daemon=True).start()

def run_timer():
    global remaining_time, time_running, paused
    while remaining_time > 0 and time_running:
        if not paused:
            mins, secs = divmod(remaining_time, 60)
            hrs, mins = divmod(mins, 60)
            timer_label.configure(text=f"{hrs:02}:{mins:02}:{secs:02}")
            time.sleep(1)
            remaining_time -= 1
        else:
            time.sleep(0.2)
    if remaining_time <= 0:
        timer_label.configure(text="00:00:00")
        time_running = False

def pause_timer():
    global paused
    paused = True

def resume_timer():
    global paused
    paused = False

def reset_timer():
    global time_running, paused, remaining_time
    time_running = False
    paused = False
    remaining_time = 0
    timer_label.configure(text="00:00:00")

# --- UI ---
ctk.CTkLabel(root, text="Set Time", font=("Arial", 18)).pack(pady=10)

frame = ctk.CTkFrame(root)
frame.pack(pady=10)

ctk.CTkEntry(frame, textvariable=hours_var, width=60).grid(row=0, column=0, padx=5)
ctk.CTkLabel(frame, text="h").grid(row=1, column=0)

ctk.CTkEntry(frame, textvariable=minutes_var, width=60).grid(row=0, column=1, padx=5)
ctk.CTkLabel(frame, text="m").grid(row=1, column=1)

ctk.CTkEntry(frame, textvariable=seconds_var, width=60).grid(row=0, column=2, padx=5)
ctk.CTkLabel(frame, text="s").grid(row=1, column=2)

timer_label = ctk.CTkLabel(root, text="00:00:00", font=("Arial", 36))
timer_label.pack(pady=20)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="Start", command=start_timer).grid(row=0, column=0, padx=5)
ctk.CTkButton(btn_frame, text="Pause", command=pause_timer).grid(row=0, column=1, padx=5)
ctk.CTkButton(btn_frame, text="Resume", command=resume_timer).grid(row=0, column=2, padx=5)
ctk.CTkButton(btn_frame, text="Reset", command=reset_timer).grid(row=0, column=3, padx=5)

root.mainloop()
