import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

COLOR_GRAY_500 = (107, 114, 128)
COLOR_GRAY_600 = (75, 85, 99)
COLOR_GRAY_700 = (55, 65, 81)
COLOR_SLATE_500 = (100, 116, 139)
COLOR_ZINC_500 = (113, 113, 122)
COLOR_STONE_500 = (120, 113, 108)
COLOR_BLUE_GRAY_500 = (92, 107, 122)

COLORS = [
    COLOR_GRAY_500,
    COLOR_GRAY_600,
    COLOR_GRAY_700,
    COLOR_SLATE_500,
    COLOR_ZINC_500,
    COLOR_STONE_500,
    COLOR_BLUE_GRAY_500,
]

AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 100
AVATAR_TEXT_VERTICAL_OFFSET = 10
AVATAR_TEXT_COLOR = (255, 255, 255)


def generate_avatar(name):
    letter = name[0].upper() if name else "?"
    color = random.choice(COLORS)
    image = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (
        (AVATAR_SIZE - text_width) / 2,
        (AVATAR_SIZE - text_height) / 2 - AVATAR_TEXT_VERTICAL_OFFSET,
    )
    draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
