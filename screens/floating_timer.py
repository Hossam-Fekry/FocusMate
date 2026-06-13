import customtkinter as ctk


class FloatingTimer(ctk.CTkToplevel):
    def __init__(self, controller, manager):
        super().__init__(controller)

        self.controller = controller
        self.manager = manager

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

        self.pause_btn = ctk.CTkButton(
            self.frame,
            text="⏸",
            width=40,
            height=30,
            corner_radius=10,
            command=self.toggle_pause
    )
        self.pause_btn.pack(pady=(0, 10))

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
        if not self.winfo_exists():
            return

        # Always show real time
        time_text = self.manager.format_time(self.manager.time_left)
        self.label.configure(text=time_text)
        
        if self.manager.is_paused:
            self.pause_btn.configure(text="▶")
        else:
            self.pause_btn.configure(text="⏸")

        self.after(500, self.update_ui)

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
    
    def toggle_pause(self):
        self.manager.pause()
        
    def destroy(self):
        # Clear the reference in controller before destroying
        if hasattr(self.controller, 'floating_timer'):
            self.controller.floating_timer = None
        super().destroy()
