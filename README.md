# FocusMate

FocusMate is a productivity app designed to help you manage your time, tasks, and goals efficiently. It combines a Pomodoro timer, to-do list, daily goals, and statistics tracking in a single, user-friendly interface.

---

## Features

- **Pomodoro Timer:** Boost your focus using the Pomodoro technique.
- **To-Do List:** Organize and prioritize your daily tasks.
- **Daily Goals:** Set and track your personal goals.
- **Statistics:** Visualize your productivity and achievements.
- **Customizable Settings:** Personalize the app to fit your workflow.
- **Modern UI:** Built with [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for a sleek, dark/light mode interface.
- **Splash Screen:** Welcoming splash screen on startup.
- **Navigation Bar:** Quick access to all main features.

---

## Project Structure

```
FocusMate/
│
├── main.py                 # Main entry point of the app
│
├── assets/                 # Static files (icons, images...)
│   ├── logo.ico
│   ├── logo.png
│   └── icons/
│       ├── pomodoro-timer.png
│       ├── todo-list.png
│       ├── goals.png
│       ├── stats.png
│       ├── settings.png
│       ├── counter.png
│       └── custom-timer.png
│
├── data/                   # JSON data files
│   ├── tasks.json          # To-Do List data
│   ├── goals.json          # Daily goals
│   ├── progress.json       # Study time sessions (by date/minutes)
│   └── settings.json       # User preferences (theme, etc.)
│
├── screens/                # Each screen as a separate file
│   ├── __init__.py
│   ├── home.py             # Dashboard screen
│   ├── pomodoro.py         # Pomodoro timer screen
│   ├── todo.py             # To-Do List screen
│   ├── goals.py            # Daily goals screen
│   ├── stats.py            # Statistics screen
│   ├── settings.py         # Settings screen
│   ├── counter.py          # Counter screen
│   └── custom-timer.py     # Custom timer screen
│
├── utils/                  # Helper functions
│   ├── __init__.py
│   └── ui_function.py      # UI helpers (e.g., center_window)
│
├── testing/                # Experiments and samples (not required to run app)
│
├── splash_screen_start.py  # Splash screen entry point (optional)
├── requirements.txt        # Dependencies (customtkinter, Pillow, matplotlib)
└── README.md               # Documentation
```

---

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Hossam-Fekry/FocusMate.git
   cd FocusMate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   python splash_screen_start.py
   ```
   Or, to skip the splash screen:
   ```sh
   python main.py
   ```

---

## Dependencies

- `customtkinter`
- `Pillow`
- `matplotlib`
- (See `requirements.txt` for the full list.)

---

## Screenshots

> _Add screenshots of your home page, splash screen, and main features here for better presentation._

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## File Directory

The full file directory is shown above in the **Project Structure** section for easy reference.
