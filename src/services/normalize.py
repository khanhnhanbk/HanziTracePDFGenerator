
# Danh sách các dấu câu cần lọc bỏ khỏi ô tập viết (cả tiếng Anh/Việt và tiếng Trung)
PUNCTUATION_LIST = [
    ',', '.', '...', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']',
    '，', '。', '、', '！', '？', '；', '：', '“', '”', '‘', '’', '（', '）', '…'
]

def normalizer(raw_text:str) -> str:
    for punct in PUNCTUATION_LIST:
        raw_text = raw_text.replace(punct, "")
    
    # Remove whitespace and split into characters
    characters = "".join(raw_text.split())
    
    # Use a set to track seen characters and a list to maintain order
    seen = set()
    unique_characters = []
    for char in characters:
        if char not in seen:
            seen.add(char)
            unique_characters.append(char)
    
    return "".join(unique_characters)