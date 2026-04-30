import customtkinter as ctk


class FloatingTimer(ctk.CTkToplevel):
    def __init__(self, parent, pomodoro_instance):
        super().__init__(parent)

        self.pomodoro = pomodoro_instance

        # 🪟 Window setup
        self.geometry("220x110")
        self.title("FocusMate Timer")
        self.attributes("-topmost", True)
        self.resizable(False, False)

        # 🔥 Make it look like widget
        self.overrideredirect(True)
        self.attributes("-alpha", 0.95)

        # 🧱 UI Frame
        self.frame = ctk.CTkFrame(self, corner_radius=15)
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ⏱️ Timer label
        self.label = ctk.CTkLabel(
            self.frame,
            text="00:00",
            font=("Arial", 28, "bold")
        )
        self.label.pack(expand=True)

        # ❌ Close button
        self.close_btn = ctk.CTkButton(
            self.frame,
            text="✕",
            width=25,
            height=25,
            corner_radius=50,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.destroy
        )
        self.close_btn.place(x=160, y=5)

        # 🖱️ Dragging
        self.frame.bind("<Button-1>", self.start_move)
        self.frame.bind("<B1-Motion>", self.do_move)

        # Bring to front
        self.lift()
        self.focus_force()

        # Start updating
        self.update_ui()

    # --------------------------
    # 🔄 Update Timer
    # --------------------------
    def update_ui(self):
        try:
            # Always show real time
            time_text = self.pomodoro.format_time(self.pomodoro.time_left)
            self.label.configure(text=time_text)

        except:
            # If something breaks (screen destroyed)
            self.destroy()
            return

        self.after(1000, self.update_ui)

    # --------------------------
    # 🖱️ Dragging Logic
    # --------------------------
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f"+{x}+{y}")