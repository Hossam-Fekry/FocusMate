import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.title("Statistics - FocusMate")
app.geometry("500x400")

# Title
title = ctk.CTkLabel(app, text="📊 Study Statistics", font=("Arial", 20, "bold"))
title.pack(pady=15)

# Matplotlib chart
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
sessions = [4, 5, 2, 6, 3, 7, 5]

fig, ax = plt.subplots(figsize=(4, 2.5))
ax.bar(days, sessions)
ax.set_title("Pomodoro Sessions per Day")
ax.set_ylabel("Sessions")

canvas = FigureCanvasTkAgg(fig, master=app)
canvas.get_tk_widget().pack()
canvas.draw()

app.mainloop()
