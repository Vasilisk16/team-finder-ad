import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


COLORS = [
    (107, 114, 128),
    (75, 85, 99),
    (55, 65, 81),
    (100, 116, 139),
    (113, 113, 122),
    (120, 113, 108),
    (92, 107, 122),
]


def generate_avatar(name):
    letter = name[0].upper() if name else "?"
    color = random.choice(COLORS)
    size = 200
    image = Image.new("RGB", (size, size), color)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2 - 10)
    draw.text(position, letter, fill=(255, 255, 255), font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{letter}.png")
