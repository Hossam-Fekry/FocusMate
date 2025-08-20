import customtkinter as ctk
import time

# إعداد النافذة
app = ctk.CTk()
app.geometry("400x200")
app.title("Digital Clock")

# دالة لتحديث الساعة
def update_time():
    current_time = time.strftime("%H:%M")  # الساعات والدقايق
    clock_label.configure(text=current_time)
    app.after(1000, update_time)  # تحدث كل ثانية

# اللابل بتاع الساعة
clock_label = ctk.CTkLabel(app, text="", font=("DS-Digital", 60, "bold"))
clock_label.pack(pady=40)

# تشغيل التحديث أول مرة
update_time()

app.mainloop()
