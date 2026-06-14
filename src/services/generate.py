import csv
import math
import os
import sys
from pathlib import Path
import re

from pypinyin import pinyin, Style
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from src.datas.usersetting import UserSettings
from src.datas.usersetting import SeparatorEnum

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

FONT_PATH = BASE_DIR / "statics" / "fonts" / "Kaiti.ttf"
PYIYIN_FONT = BASE_DIR / "statics" / "fonts" / "SpaceGrotesk.ttf"


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


def draw_character(c, char, x, y, size, font_name, column_index,phrase_index, trace_columns):
    font_size = size * 0.75
    c.setFont(font_name, font_size)
    text_width = pdfmetrics.stringWidth(char, font_name, font_size)
    text_x = x + (size - text_width) / 2
    text_y = y + (size - font_size) / 2 + font_size * 0.2

    if phrase_index == 0:
        c.setFillColorRGB(0, 0, 0)
        c.drawString(text_x, text_y, char)
    elif phrase_index < trace_columns:
        c.setFillColorRGB(0.6, 0.6, 0.6)
        c.drawString(text_x, text_y, char)


def parse_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def generate_chinese_practice_sheet(
    characters="你好", user_settings: UserSettings | None = None
):
    if user_settings is None:
        user_settings = UserSettings()

    if user_settings.multi_char_line:
        sep = getattr(user_settings, "separator", SeparatorEnum.ENTER)
        if sep == SeparatorEnum.ENTER:
            tokens = parse_lines(characters)
        elif sep == SeparatorEnum.COMMA:
            tokens = [t.strip() for t in re.split(r"[\n,]+", characters) if t.strip()]
        elif sep == SeparatorEnum.SEMICOLON:
            tokens = [t.strip() for t in re.split(r"[\n;；]+", characters) if t.strip()]
        elif sep == SeparatorEnum.ANY:
            tokens = [t.strip() for t in re.split(r"[\n,;，；、]+", characters) if t.strip()]
        elif sep == SeparatorEnum.NONE:
            tokens = [characters] if characters and characters.strip() else []
        else:
            tokens = parse_lines(characters)
        lines = tokens
    else:
        lines = [c for c in characters if not c.isspace()]

    filename = Path(user_settings.output_directory) / user_settings.output_filename
    # Ensure filename has .pdf suffix
    if not filename.suffix:
        filename = filename.with_suffix(".pdf")
    # Ensure output directory exists
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    # ReportLab expects a string path or file-like object
    filename_str = str(filename)

    if not lines:
        raise ValueError("No characters were provided for the practice sheet.")

    pdfmetrics.registerFont(TTFont("KaiTi", FONT_PATH))
    font_name = "KaiTi"

    pdfmetrics.registerFont(TTFont("PinyinFont", PYIYIN_FONT))
    pinyin_font_name = "PinyinFont"

    c = canvas.Canvas(filename_str, pagesize=A4)
    width, height = A4

    margin_left = user_settings.margin_left
    margin_top = user_settings.margin_top
    grid_size = user_settings.grid_size

    usable_width = width - margin_left * 2
    usable_height = height - margin_top * 2

    cols_per_page = int(usable_width // grid_size)
    rows_per_page = int(usable_height // grid_size)
    page_count = math.ceil(len(lines) / rows_per_page)

    start_y = height - margin_top
    for page in range(page_count):
        index_offset = page * rows_per_page

        for row in range(rows_per_page):
            current_y = start_y - (row * grid_size) - grid_size
            line_index = index_offset + row

            line_text = lines[line_index] if line_index < len(lines) else ""
            if line_text and user_settings.show_pinyin:
                draw_pinyin(
                    pinyin_font_name, c, margin_left, grid_size, current_y, line_text
                )

            for col in range(1, cols_per_page):
                current_x = margin_left + (col * grid_size)

                draw_mizige_box(c, current_x, current_y, grid_size)

                if not line_text:
                    continue

                phrase_length = len(line_text)
                char = line_text[(col - 1) % phrase_length]
                phrase_index = (col - 1) // phrase_length

                if char:
                    draw_character(
                        c,
                        char,
                        current_x,
                        current_y,
                        grid_size,
                        font_name,
                        col,
                        phrase_index,
                        user_settings.trace_columns,
                    )

        if page < page_count - 1:
            c.showPage()

    c.save()
    print(f"Success: Sheet saved as '{filename_str}'")


def draw_pinyin(pinyin_font_name, c, margin_left, grid_size, current_y, char):
    char_pinyin = get_pinyin(char)
    # choose a readable font size and wrap pinyin if it's too long
    font_size = max(8, int(grid_size / 4))
    c.setFont(pinyin_font_name, font_size)
    c.setFillColorRGB(0, 0, 0)

    available_width = grid_size - 4
    tokens = char_pinyin.split()
    lines = []
    current = ""
    for tok in tokens:
        test = (current + " " + tok).strip() if current else tok
        if pdfmetrics.stringWidth(test, pinyin_font_name, font_size) <= available_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = tok
    if current:
        lines.append(current)

    line_height = font_size * 0.95
    start_y = current_y + grid_size * 0.6 + (len(lines) - 1) * line_height
    pinyin_x = margin_left - 5
    for i, line in enumerate(lines):
        pinyin_y = start_y - i * line_height
        c.drawString(pinyin_x, pinyin_y, line)
