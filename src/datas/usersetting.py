from dataclasses import dataclass, field
from enum import Enum, unique

import os

# enum for separator
class SeparatorEnum(Enum):
    ENTER = '\n'
    COMMA = ','
    SEMICOLON = ';'
    ANY = 'ANY'
    
@dataclass
class UserSettings:
    grid_size: int = 45
    trace_columns: int = 10
    multi_char_line: bool = False
    separator: SeparatorEnum = SeparatorEnum.ENTER

    show_pinyin: bool = True
    show_wubi:bool = True

    margin_left: int = 25
    margin_top: int = 35
    output_directory: str = field(default_factory=os.getcwd)
    output_filename: str = "output.pdf"
