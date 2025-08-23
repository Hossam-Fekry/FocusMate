import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os
from datetime import date

DATA_FILE = "progress.json"


# ----------------- حفظ واسترجاع البيانات -----------------
def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(DATA_FILE, "w") as f:
        json.dump(progress, f)


def add_study_minutes(minutes):
    progress = load_progress()
    today = str(date.today())

    if today not in progress:
        progress[today] = 0

    progress[today] += minutes
    save_progress(progress)


# ----------------- نافذة التطبيق -----------------
class FocusMate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FocusMate - Progress Chart")
        self.geometry("600x400")

        # زر يضيف دقائق (مثال تجريبي بدل المؤقت)
        self.add_btn = ctk.CTkButton(self, text="Add 25 min (Pomodoro)", command=self.add_progress)
        self.add_btn.pack(pady=10)

        # زر تحديث الرسم
        self.chart_btn = ctk.CTkButton(self, text="Show Chart", command=self.show_chart)
        self.chart_btn.pack(pady=10)

        # فريم للرسم
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_progress(self):
        add_study_minutes(25)

    def show_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        progress = load_progress()
        if not progress:
            label = ctk.CTkLabel(self.chart_frame, text="No progress yet.")
            label.pack()
            return

        # تجهيز البيانات
        dates = list(progress.keys())
        minutes = list(progress.values())

        # عمل الرسمة
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(dates, minutes)
        ax.set_title("Study Progress")
        ax.set_ylabel("Minutes")

        # دمج الرسم مع tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# ----------------- تشغيل التطبيق -----------------
if __name__ == "__main__":
    app = FocusMate()
    app.mainloop()
