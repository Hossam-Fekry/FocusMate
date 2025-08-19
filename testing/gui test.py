import tkinter as tk

def on_click(event):
    print("Circle button clicked!")

root = tk.Tk()
root.title("Circle Button Example")

canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=0)
canvas.pack()

# رسم دائرة
circle = canvas.create_oval(50, 50, 150, 150, fill="skyblue", outline="")

# إضافة نص في النص
text = canvas.create_text(100, 100, text="Start", font=("Arial", 14, "bold"))

# ربط الدائرة والنص بالضغط
canvas.tag_bind(circle, "<Button-1>", on_click)
canvas.tag_bind(text, "<Button-1>", on_click)

root.mainloop()
