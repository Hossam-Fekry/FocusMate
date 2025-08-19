import customtkinter as ctk

ctk.set_appearance_mode("light")

app = ctk.CTk()
app.title("Daily Goal - FocusMate")
app.geometry("400x400")

# Title
title = ctk.CTkLabel(app, text="🎯 Daily Goal", font=("Arial", 20, "bold"))
title.pack(pady=15)

# Input for goal
goal_label = ctk.CTkLabel(app, text="Set your goal (Pomodoro sessions):")
goal_label.pack(pady=5)

goal_entry = ctk.CTkEntry(app, placeholder_text="e.g. 6")
goal_entry.pack(pady=5)

# Progress
progress_label = ctk.CTkLabel(app, text="Progress:")
progress_label.pack(pady=5)

progressbar = ctk.CTkProgressBar(app, width=250)
progressbar.set(0.5)  # 50% progress
progressbar.pack(pady=10)

progress_text = ctk.CTkLabel(app, text="3 / 6 sessions completed ✅")
progress_text.pack(pady=5)

# Save button
save_btn = ctk.CTkButton(app, text="Save Goal")
save_btn.pack(pady=20)

app.mainloop()
