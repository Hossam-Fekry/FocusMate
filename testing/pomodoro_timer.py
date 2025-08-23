import customtkinter as ctk
import time
import threading

# إعداد الواجهة
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Pomodoro Timer")
root.geometry("400x300")

# المتغيرات
running = False
paused = False
time_left = 25 * 60   # 25 دقيقة

# تحديث عرض الوقت
def update_timer_label():
    mins, secs = divmod(time_left, 60)
    timer_label.configure(text=f"{mins:02d}:{secs:02d}")

# تشغيل المؤقت
def start_timer():
    global running, paused
    if not running:
        running = True
        paused = False
        threading.Thread(target=run_timer, daemon=True).start()

# المؤقت نفسه
def run_timer():
    global time_left, running, paused
    while running and time_left > 0:
        if not paused:
            time.sleep(1)
            time_left -= 1
            update_timer_label()
        else:
            time.sleep(0.2)

# إيقاف مؤقت مؤقت (Pause)
def pause_timer():
    global paused
    paused = not paused
    if paused:
        pause_btn.configure(text="Resume")
    else:
        pause_btn.configure(text="Pause")

# إعادة تعيين المؤقت
def reset_timer():
    global running, paused, time_left
    running = False
    paused = False
    time_left = 25 * 60
    update_timer_label()
    pause_btn.configure(text="Pause")

# واجهة المستخدم
timer_label = ctk.CTkLabel(root, text="25:00", font=("Arial", 48))
timer_label.pack(pady=40)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=20)

start_btn = ctk.CTkButton(btn_frame, text="Start", command=start_timer)
start_btn.grid(row=0, column=0, padx=10)

pause_btn = ctk.CTkButton(btn_frame, text="Pause", command=pause_timer)
pause_btn.grid(row=0, column=1, padx=10)

reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=reset_timer)
reset_btn.grid(row=0, column=2, padx=10)

update_timer_label()

root.mainloop()
