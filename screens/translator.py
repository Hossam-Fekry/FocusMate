from customtkinter import *
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_function import center_window
import subprocess
import PIL.Image as Image
import requests
from langdetect import detect

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "settings.json")

# -------------------------------------------------------
#               TRANSLATION CACHE (Speed Booster)
# -------------------------------------------------------
translated_texts = {}  # cache dictionary

def get_cached_translation(text, source, target):
    key = f"{text}|||{source}|||{target}"
    return translated_texts.get(key)

def save_translation_to_cache(text, source, target, translated):
    key = f"{text}|||{source}|||{target}"
    translated_texts[key] = translated
# -------------------------------------------------------


def load_settings():
    with open(SETTINGS_FILE, "r") as file:
        settings = json.load(file)
        return settings["theme"]


def go_back(event=None):
    root.destroy()
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "..", "screens", "home.py")])


def translate_text(textToTranslate, source_language, targetLanguage):
    url = "https://api.mymemory.translated.net/get"
    params = {"q": textToTranslate, "langpair": f"{source_language}|{targetLanguage}"}

    result = requests.get(url, params=params).json()
    return result["responseData"]["translatedText"]


root = CTk()
root.title("FocusMate - Translator")
root.geometry("950x600")
set_appearance_mode(load_settings())
root.iconbitmap("assets/icons/translator.ico")

back_icon = CTkImage(dark_image=Image.open("./assets/icons/back.png"), size=(25, 25))
right_arrow_icon = CTkImage(dark_image=Image.open("./assets/icons/right_arrow.png"), size=(35, 35))
translator_image = CTkImage(dark_image=Image.open("./assets/icons/translator.png"), size=(150, 150))

CTkLabel(root, image=translator_image, text="", font=("Arial", 24, "bold")).pack(pady=50)
center_window(root, 800, 600)

language_menu = CTkOptionMenu(
    root,
    values=["auto", "en", "es", "fr", "de", "it", "ja", "ko", "pt", "ru", "tr", "zh", "ar"],
    width=200, height=30,
    fg_color="#1E1E1E",
    button_color="#1E1E1E",
    button_hover_color="#333333",
    dropdown_fg_color="#1E1E1E",
    dropdown_hover_color="#333333",
    dropdown_text_color="white",
)
language_menu.place(x=70, y=235)
language_menu.set("auto")

target_menu = CTkOptionMenu(
    root,
    values=["en", "es", "fr", "de", "it", "ja", "ko", "pt", "ru", "tr", "zh", "ar"],
    width=200, height=30,
    fg_color="#1E1E1E",
    button_color="#1E1E1E",
    button_hover_color="#333333",
    dropdown_fg_color="#1E1E1E",
    dropdown_hover_color="#333333",
    dropdown_text_color="white",
)
target_menu.place(x=500, y=235)
target_menu.set("ar")

main_frame = CTkFrame(root, height=400, fg_color="#1E1E1E")
main_frame.pack(fill="x", side="bottom")

input_box = CTkTextbox(main_frame, width=350, height=300, fg_color="#2A2A2A", font=("Arial", 14))
input_box.pack(side="left", padx=10, pady=10)

right_arrow_label = CTkLabel(main_frame, text="", image=right_arrow_icon)
right_arrow_label.pack(side="left", padx=10, pady=10)

output_box = CTkTextbox(main_frame, width=350, height=300, fg_color="#2A2A2A", font=("Arial", 14), state="disabled")
output_box.pack(side="right", padx=10, pady=10)

back_button = CTkButton(
    root,
    text="",
    image=back_icon,
    fg_color="transparent",
    hover_color="#333333",
    command=go_back,
    width=40, height=40
)
back_button.place(x=10, y=10)


# -------------------------------------------------------
#                THE UPDATED TRANSLATION SYSTEM
# -------------------------------------------------------
def uptade_output(event=None):
    text = input_box.get("1.0", "end-1c").strip()
    target_lang = target_menu.get()
    source_option = language_menu.get()

    # Clear output if empty
    if text == "":
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.configure(state="disabled")
        return

    # Auto detect
    if source_option == "auto":
        source_lang = detect(text)
    else:
        source_lang = source_option

    # --------- Check Cache First (Speed!) ----------
    cached = get_cached_translation(text, source_lang, target_lang)
    if cached:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", cached)
        output_box.configure(state="disabled")
        return

    # --------- Translate Normally ----------
    translated = translate_text(text, source_lang, target_lang)

    # Save to cache
    save_translation_to_cache(text, source_lang, target_lang, translated)

    # Show output
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", translated)
    output_box.configure(state="disabled")


typing_delay = None

def on_user_typing(event=None):
    global typing_delay
    if typing_delay:
        root.after_cancel(typing_delay)

    typing_delay = root.after(500, uptade_output)


input_box.bind("<KeyRelease>", on_user_typing)

root.bind('<Escape>', go_back)

root.mainloop()
