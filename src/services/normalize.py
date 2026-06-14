# src/services/text_normalizer.py

import re

from src.datas.usersetting import UserSettings, SeparatorEnum

# Punctuation to remove from the input text.
# If the selected separator is COMMA or SEMICOLON,
# that separator will be preserved.
PUNCTUATIONS = [
    ",",
    ".",
    "...",
    "!",
    "?",
    ";",
    ":",
    '"',
    "'",
    "(",
    ")",
    "[",
    "]",
    "，",
    "。",
    "、",
    "！",
    "？",
    "；",
    "：",
    "“",
    "”",
    "‘",
    "’",
    "（",
    "）",
    "…",
]

# Supported characters:
# - Chinese characters
# Map common fullwidth punctuation to ASCII equivalents for consistent handling
FULLWIDTH_TO_ASCII = str.maketrans(
    {
        "，": ",",
        "。": ".",
        "；": ";",
        "：": ":",
        "！": "!",
        "？": "?",
        "（": "(",
        "）": ")",
        "、": ",",
    }
)

# - Latin letters
# - Numbers
# - Middle dot (·)
ALLOWED_RE = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFFA-Za-z0-9·]")


def remove_punctuation(text: str, separator: SeparatorEnum) -> str:
    """
    Remove punctuation except the configured separator.
    """
    punctuations = PUNCTUATIONS.copy()

    # Equivalents for separators (ASCII and fullwidth)
    separator_equivalents = {
        SeparatorEnum.COMMA: [",", "，"],
        SeparatorEnum.SEMICOLON: [";", "；"],
        SeparatorEnum.ENTER: ["\n"],
        SeparatorEnum.ANY: [",", "，",";", "；","\n"],
    }

    equivalents = separator_equivalents.get(separator)
    if equivalents:
        for ch in equivalents:
            if ch in punctuations:
                punctuations.remove(ch)

    for p in punctuations:
        text = text.replace(p, "")

    return text


def clean_token(token: str) -> str:
    """
    Remove whitespace and unsupported characters.
    """
    token = "".join(token.split())

    return "".join(ch for ch in token if ALLOWED_RE.match(ch))


def split_tokens(text: str, separator: SeparatorEnum) -> list[str]:
    """
    Split text according to user separator settings.
    """
    if separator == SeparatorEnum.ENTER:
        return text.splitlines()

    # Treat ASCII and fullwidth variants as equivalent when splitting
    if separator == SeparatorEnum.COMMA:
        return re.split(r"[,，]+", text)

    if separator == SeparatorEnum.SEMICOLON:
        return re.split(r"[;；]+", text)

    # SeparatorEnum.ANY (include fullwidth comma/semicolon)
    return re.split(r"[\s,;，；]+", text)


def unique_preserve_order(items: list[str]) -> list[str]:
    """
    Remove duplicates while preserving order.
    """
    seen = set()
    result = []

    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)

    return result


def normalize_multi_char_text(
    text: str,
    separator: SeparatorEnum,
) -> str:
    """
    Normalize text as words/tokens.
    Example:
        你好,你好,中国
    =>
        你好,中国
    """
    tokens = split_tokens(text, separator)

    cleaned_tokens = [clean_token(token) for token in tokens]

    cleaned_tokens = unique_preserve_order(cleaned_tokens)

    separator_map = {
        SeparatorEnum.ENTER: "\n",
        SeparatorEnum.COMMA: ",",
        SeparatorEnum.SEMICOLON: ";",
        SeparatorEnum.ANY: ",",
    }

    output_separator = separator_map.get(separator, " ")

    return output_separator.join(cleaned_tokens)


def normalize_single_char_text(text: str) -> str:
    """
    Normalize text as individual characters.
    Example:
        你你好好中国
    =>
        你好中国
    """
    text = clean_token(text)

    seen = set()
    result = []

    for ch in text:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)

    return "".join(result)


def normalizer(
    raw_text: str,
    user_settings: UserSettings,
) -> str:
    """
    Main normalization entry point.
    """

    if not raw_text:
        return ""

    # Normalize fullwidth punctuation to ASCII equivalents first
    raw_text = raw_text.translate(FULLWIDTH_TO_ASCII)

    # Remove punctuation
    raw_text = remove_punctuation(
        raw_text,
        user_settings.separator,
    )

    if user_settings.multi_char_line:
        return normalize_multi_char_text(
            raw_text,
            user_settings.separator,
        )

    return normalize_single_char_text(raw_text)
