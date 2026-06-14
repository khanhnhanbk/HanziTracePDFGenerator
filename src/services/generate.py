import math
import sys
from pathlib import Path
import re

from pypinyin import pinyin
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from src.datas.usersetting import UserSettings
from src.datas.usersetting import SeparatorEnum
from src.services.normalize import normalizer

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

FONT_PATH = BASE_DIR / "statics" / "fonts" / "Kaiti.ttf"
PYIYIN_FONT = BASE_DIR / "statics" / "fonts" / "SpaceGrotesk.ttf"


def parse_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def get_pinyin(char):
    return " ".join([item[0] for item in pinyin(char)])


def build_output_file(
    output_directory: str,
    output_filename: str,
) -> str:
    """
    Build a safe PDF output path.

    If the directory or filename is invalid,
    fall back to ./output.pdf
    """

    try:
        filename = (output_filename or "").strip()

        if not filename:
            filename = "output.pdf"

        path = Path(output_directory or ".") / filename

        if path.suffix.lower() != ".pdf":
            path = path.with_suffix(".pdf")

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        return str(path)

    except Exception:
        return str(Path.cwd() / "output.pdf")


class ChinesePracticeSheetGenerator:

    pdfmetrics.registerFont(TTFont("KaiTi", FONT_PATH))
    pdfmetrics.registerFont(TTFont("PinyinFont", PYIYIN_FONT))
    CHAR_FONT = "KaiTi"
    PINYIN_FONT = "PinyinFont"
    BLACK = (0, 0, 0)
    GRAY = (0.6, 0.6, 0.6)
    RED = (0.8, 0.4, 0.4)

    def __init__(self, characters: str, user_settings: UserSettings):
        self.characters = normalizer(
            characters,
            user_settings,
        )

        self.settings = user_settings
        self.filename = build_output_file(
            user_settings.output_directory, user_settings.output_filename
        )
        self.pdf_canvas = canvas.Canvas(self.filename, pagesize=A4)
        width, height = A4
        usable_width = width - user_settings.margin_left * 2
        usable_height = height - user_settings.margin_top * 2

        self.cols_per_page = int(usable_width // user_settings.grid_size)
        self.rows_per_page = int(usable_height // user_settings.grid_size)

    def draw_mizige_box(self, x, y):
        c = self.pdf_canvas
        size = self.settings.grid_size

        c.setStrokeColorRGB(*self.RED)

        c.setLineWidth(1.2)
        c.rect(x, y, size, size, stroke=1, fill=0)

        c.setLineWidth(0.5)
        c.setDash(2, 2)

        c.line(x, y + size / 2, x + size, y + size / 2)
        c.line(x + size / 2, y, x + size / 2, y + size)
        c.line(x, y, x + size, y + size)
        c.line(x, y + size, x + size, y)

        c.setDash()

    def draw_character(self, char: str, x: int, y: int, phrase_index: int):
        c = self.pdf_canvas
        size = self.settings.grid_size
        font_size = size * 0.75

        c.setFont(self.CHAR_FONT, font_size)
        text_width = pdfmetrics.stringWidth(char, self.CHAR_FONT, font_size)

        text_x = x + (size - text_width) / 2
        text_y = y + (size - font_size) / 2 + font_size * 0.2

        if phrase_index == 0:
            c.setFillColorRGB(*self.BLACK)
            c.drawString(text_x, text_y, char)
        elif phrase_index < self.settings.trace_columns:
            c.setFillColorRGB(*self.GRAY)
            c.drawString(text_x, text_y, char)

    def get_lines(self) -> list[str]:

        if self.settings.multi_char_line:
            sep = self.settings.separator

            if sep == SeparatorEnum.ENTER:
                tokens = parse_lines(self.characters)
            elif sep == SeparatorEnum.COMMA:
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n,，]+", self.characters)
                    if t.strip()
                ]
            elif sep == SeparatorEnum.SEMICOLON:
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n;；]+", self.characters)
                    if t.strip()
                ]
            else:  # sep == SeparatorEnum.ANY
                tokens = [
                    t.strip()
                    for t in re.split(r"[\n,;，；、]+", self.characters)
                    if t.strip()
                ]

            lines = tokens
        else:
            lines = [c for c in self.characters if not c.isspace()]

        if not lines:
            raise ValueError("No characters were provided for the practice sheet.")
        return lines

    def build_render_rows(self, lines) -> list[tuple[str, int]]:
        """
        Returns:
            [
                ("你好", 0),
                ("你好", 11),
                ("中国", 0),
                ...
            ]

        tuple:
            (phrase, start_index)
        """

        rows = []

        usable_cells = self.cols_per_page - 1

        for phrase in lines:
            phrase_length = len(phrase)

            if phrase_length == 0:
                continue

            rows_needed = math.ceil(
                self.settings.trace_columns * phrase_length / usable_cells
            )

            for row in range(rows_needed):
                rows.append((phrase, row * usable_cells))

        return rows

    def draw_empty_row(self, current_y):
        for col in range(1, self.cols_per_page):
            self.draw_mizige_box(
                self.settings.margin_left + self.settings.grid_size * col,
                current_y,
            )

    def draw_pinyin(self, current_y: int, char: str):
        c = self.pdf_canvas
        char_pinyin = get_pinyin(char)

        font_size = max(8, int(self.settings.grid_size / 4))
        c.setFont(self.PINYIN_FONT, font_size)
        c.setFillColorRGB(*self.BLACK)

        available_width = self.settings.grid_size - 4
        tokens = char_pinyin.split()
        lines = []
        current = ""
        for tok in tokens:
            test = (current + " " + tok).strip() if current else tok
            if (
                pdfmetrics.stringWidth(test, self.PINYIN_FONT, font_size)
                <= available_width
            ):
                current = test
            else:
                if current:
                    lines.append(current)
                current = tok
        if current:
            lines.append(current)

        line_height = font_size * 0.95
        start_y = (
            current_y + self.settings.grid_size * 0.6 + (len(lines) - 1) * line_height
        )
        pinyin_x = self.settings.margin_left - 5
        for i, line in enumerate(lines):
            pinyin_y = start_y - i * line_height
            c.drawString(pinyin_x, pinyin_y, line)

    def draw_row(self, current_y: int, line_text: str, start_index: int):

        if self.settings.show_pinyin and start_index == 0:
            self.draw_pinyin(current_y, line_text)

        for col in range(1, self.cols_per_page):
            current_x = self.settings.margin_left + (col * self.settings.grid_size)
            self.draw_mizige_box(current_x, current_y)
            phrase_length = len(line_text)

            if phrase_length == 0:
                continue
            phrase_index = (start_index + col - 1) // phrase_length

            char = line_text[(start_index + col - 1) % phrase_length]

            self.draw_character(char, current_x, current_y, phrase_index)

    def generate(self):
        lines = self.get_lines()
        c = self.pdf_canvas
        rpp = self.rows_per_page
        size = self.settings.grid_size
        render_rows = self.build_render_rows(lines)

        page_count = math.ceil(len(render_rows) / rpp)
        _, height = A4
        start_y = height - self.settings.margin_top
        for page in range(page_count):
            index_offset = page * rpp

            for row in range(rpp):
                current_y = start_y - (row * size) - size
                line_index = index_offset + row

                if line_index < len(render_rows):
                    line_text, start_index = render_rows[line_index]
                else:
                    self.draw_empty_row(current_y)
                    continue
                self.draw_row(current_y, line_text, start_index)
            if page < page_count - 1:
                c.showPage()

        c.save()
        print(f"Success: Sheet saved as '{self.filename}'")
