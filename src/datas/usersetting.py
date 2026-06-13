from dataclasses import dataclass, field
import os


@dataclass
class UserSettings:
    grid_size: int = 45
    trace_columns: int = 10

    show_pinyin: bool = True
    show_wubi:bool = True

    margin_left: int = 25
    margin_top: int = 35
    output_directory: str = field(default_factory=os.getcwd)
    output_filename: str = "output.pdf"
