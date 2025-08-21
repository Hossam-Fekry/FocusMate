import tkinter as tk
from customtkinter import CTkLabel

def center_window(window, width, height):
    """Center the Tkinter window on screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))
    window.geometry(f"{width}x{height}+{x}+{y}")

