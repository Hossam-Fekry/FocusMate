# FocusMate

FocusMate is a productivity app designed to help you manage your time, tasks, and goals efficiently. It combines a Pomodoro timer, to-do list, daily goals, and statistics tracking in a single, user-friendly interface.

---

## Features

- **Pomodoro Timer:** Boost your focus using the Pomodoro technique.
- **To-Do List:** Organize and prioritize your daily tasks.
- **Daily Goals:** Set and track your personal goals.
- **Statistics:** Visualize your productivity and achievements.
- **Customizable Settings:** Personalize the app to fit your workflow.

---

## Project Structure

```
FocusMate/
│
├── main.py                 # Main entry point of the app
│
├── assets/                 # Static files (icons, images...)
│   ├── icons/              
│   │   ├── pomodoro.png
│   │   ├── todo.png
│   │   ├── goals.png
│   │   ├── stats.png
│   │   └── settings.png
│
├── data/                   # JSON data files
│   ├── tasks.json          # To-Do List data
│   ├── goals.json          # Daily goals
│   ├── stats.json          # Study time, achievements...
│   └── settings.json       # User preferences (theme, etc.)
│
├── screens/                # Each screen as a separate file
│   ├── __init__.py
│   ├── home.py             # Dashboard screen
│   ├── pomodoro.py         # Pomodoro timer screen
│   ├── todo.py             # To-Do List screen
│   ├── goals.py            # Daily goals screen
│   ├── stats.py            # Statistics screen
│   └── settings.py         # Settings screen
│
├── testing/                  # Unit tests
│   ├── __init__.py
│   └── test_pomodoro.py    # Sample test file
│
├── requirements.txt        # Dependencies (customtkinter, matplotlib, etc.)
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
   python main.py
   ```

---

## Dependencies

- `customtkinter`
- `matplotlib`
- (See `requirements.txt` for the full list.)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## File Directory

The full file directory is shown above in the **Project Structure** section for easy reference.
