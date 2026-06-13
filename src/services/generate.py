import csv
import math
import os
from pathlib import Path

from pypinyin import pinyin, Style
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

BASE_DIR = Path(__file__).resolve().parent.parent

FONT_PATH = BASE_DIR / "statics" / "fonts" / "Kaiti.ttf"
PYIYIN_FONT = BASE_DIR / "statics" / "fonts" / "SpaceGrotesk.ttf"
TRACE_COLUMNS = 10


def get_pinyin(char):
    return " ".join([item[0] for item in pinyin(char)])


def load_characters_from_txt(filepath):
    with open(filepath, encoding="utf-8") as input_file:
        raw_text = input_file.read()
    return "".join(raw_text.split())


def load_characters_from_csv(filepath):
    characters = []
    with open(filepath, newline="", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            for cell in row:
                if cell:
                    characters.append(cell.strip())
    return "".join("".join(characters).split())


def load_characters_from_file(filepath):
    extension = os.path.splitext(filepath)[1].lower()
    if extension == ".txt":
        return load_characters_from_txt(filepath)
    if extension == ".csv":
        return load_characters_from_csv(filepath)
    raise ValueError(f"Unsupported file extension: {extension}")


def draw_mizige_box(c, x, y, size):
    c.setStrokeColorRGB(0.5, 0.1, 0.1)
    c.setLineWidth(1.2)
    c.rect(x, y, size, size, stroke=1, fill=0)

    c.setStrokeColorRGB(0.8, 0.4, 0.4)
    c.setLineWidth(0.5)
    c.setDash(2, 2)

    c.line(x, y + size / 2, x + size, y + size / 2)
    c.line(x + size / 2, y, x + size / 2, y + size)
    c.line(x, y, x + size, y + size)
    c.line(x, y + size, x + size, y)

    c.setDash()


def draw_character(
    c, char, x, y, size, font_name, column_index, trace_columns=TRACE_COLUMNS
):
    font_size = size * 0.75
    c.setFont(font_name, font_size)
    text_width = pdfmetrics.stringWidth(char, font_name, font_size)
    text_x = x + (size - text_width) / 2
    text_y = y + (size - font_size) / 2 + font_size * 0.2

    if column_index == 1:
        c.setFillColorRGB(0, 0, 0)
        c.drawString(text_x, text_y, char)
    elif column_index < trace_columns:
        c.setFillColorRGB(0.6, 0.6, 0.6)
        c.drawString(text_x, text_y, char)


def generate_chinese_practice_sheet(
    filename="chinese_practice_sheet.pdf",
    characters="永和九年岁在癸丑暮春之初初床",
):
    if isinstance(characters, (list, tuple)):
        characters = "".join(characters)

    if not characters:
        raise ValueError("No characters were provided for the practice sheet.")

    pdfmetrics.registerFont(TTFont("KaiTi", FONT_PATH))
    font_name = "KaiTi"

    pdfmetrics.registerFont(TTFont("PinyinFont", PYIYIN_FONT))
    pinyin_font_name = "PinyinFont"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    margin_left = 25
    margin_top = 35
    grid_size = 45
    usable_width = width - margin_left * 2
    usable_height = height - margin_top * 2

    cols_per_page = int(usable_width // grid_size)
    rows_per_page = int(usable_height // grid_size)
    page_count = math.ceil(len(characters) / rows_per_page)

    start_y = height - margin_top
    for page in range(page_count):
        index_offset = page * rows_per_page
        for row in range(rows_per_page):
            current_y = start_y - (row * grid_size) - grid_size
            char_index = index_offset + row
            char = characters[char_index] if char_index < len(characters) else ""

            if char:
                draw_pinyin(pinyin_font_name, c, margin_left, grid_size, current_y, char)

            for col in range(1, cols_per_page ):
                current_x = margin_left + (col * grid_size)
                draw_mizige_box(c, current_x, current_y, grid_size)
                if char:
                    draw_character(
                        c, char, current_x, current_y, grid_size, font_name, col
                    )

        if page < page_count - 1:
            c.showPage()

    c.save()
    print(f"Success: Sheet saved as '{filename}'")

def draw_pinyin(pinyin_font_name, c, margin_left, grid_size, current_y, char):
    char_pinyin = get_pinyin(char)
    c.setFont(pinyin_font_name, 12)
    c.setFillColorRGB(0,0,0)
    pinyin_x = margin_left - 5
    pinyin_y = current_y + grid_size * 0.6
    c.drawString(pinyin_x, pinyin_y, char_pinyin)
