from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# =========================
# SETTINGS
# =========================

WIDTH = 800
HEIGHT = 1000

USERNAME = "Hossam Fekry"
ACHIEVEMENT_TITLE = "14-Day Streak"
DESCRIPTION = "Completed 14 days of focus sessions"
XP_REWARD = "+100 XP"
GOLD_REWARD = "+50 Gold"
RARITY = "Rare"
DATE = "21 May 2026"

OUTPUT_FILE = "achievement_card.png"

# =========================
# CREATE BASE IMAGE
# =========================

img = Image.new("RGB", (WIDTH, HEIGHT), (40, 40, 40))
draw = ImageDraw.Draw(img)

# =========================
# COLORS
# =========================

rarity_colors = {
    "Common": (120, 120, 120),
    "Rare": (0, 120, 255),
    "Epic": (170, 0, 255),
    "Legendary": (255, 180, 0),
    "Mythic": (255, 40, 40)
}

main_color = rarity_colors.get(RARITY, (255, 255, 255))

# =========================
# FONTS
# =========================

# Windows font path
FONT_PATH = "C:/Windows/Fonts/arial.ttf"

title_font = ImageFont.truetype(FONT_PATH, 60)
subtitle_font = ImageFont.truetype(FONT_PATH, 30)
small_font = ImageFont.truetype(FONT_PATH, 24)
username_font = ImageFont.truetype(FONT_PATH, 40)

# =========================
# TOP BANNER
# =========================

banner_height = 280

draw.rectangle(
    [(0, 0), (WIDTH, banner_height)],
    fill=(90, 80, 90)
)

# =========================
# AVATAR CIRCLE
# =========================

avatar_size = 140
avatar_x = WIDTH // 2 - avatar_size // 2
avatar_y = 110

draw.ellipse(
    [(avatar_x, avatar_y),
     (avatar_x + avatar_size, avatar_y + avatar_size)],
    fill=(0, 0, 0),
    outline=main_color,
    width=6
)

draw.text(
    (WIDTH // 2, avatar_y + 55),
    "Avatar",
    fill="white",
    anchor="mm",
    font=small_font
)

# =========================
# MAIN CARD AREA
# =========================

card_y = 240

draw.rectangle(
    [(0, card_y), (WIDTH, HEIGHT)],
    fill=(70, 70, 70)
)

# =========================
# ACHIEVEMENT TITLE
# =========================

draw.text(
    (WIDTH // 2, 380),
    ACHIEVEMENT_TITLE,
    fill="white",
    anchor="mm",
    font=title_font
)

# =========================
# DESCRIPTION
# =========================

draw.text(
    (WIDTH // 2, 470),
    DESCRIPTION,
    fill=(220, 220, 220),
    anchor="mm",
    font=subtitle_font
)

# =========================
# RARITY TEXT
# =========================

draw.text(
    (WIDTH // 2, 560),
    RARITY,
    fill=main_color,
    anchor="mm",
    font=subtitle_font
)

# =========================
# REWARDS
# =========================

draw.text(
    (WIDTH // 2, 650),
    f"{XP_REWARD}   •   {GOLD_REWARD}",
    fill=(255, 220, 100),
    anchor="mm",
    font=subtitle_font
)

# =========================
# DATE
# =========================

draw.text(
    (WIDTH // 2, 740),
    f"Unlocked: {DATE}",
    fill=(200, 200, 200),
    anchor="mm",
    font=small_font
)

# =========================
# USERNAME
# =========================

draw.text(
    (WIDTH // 2, 900),
    USERNAME,
    fill="white",
    anchor="mm",
    font=username_font
)

# =========================
# GLOW EFFECT
# =========================

glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow)

glow_draw.rounded_rectangle(
    [(10, 10), (WIDTH - 10, HEIGHT - 10)],
    radius=50,
    outline=main_color,
    width=10
)

glow = glow.filter(ImageFilter.GaussianBlur(12))

img = Image.alpha_composite(
    glow.convert("RGBA"),
    img.convert("RGBA")
)

# =========================
# SAVE
# =========================

img.save(OUTPUT_FILE)

print(f"Achievement card saved as: {OUTPUT_FILE}")