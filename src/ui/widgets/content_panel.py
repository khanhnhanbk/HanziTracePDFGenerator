# ui/widgets/content_panel.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class ContentPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Nhập ký tự / Nội dung:"))

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText(
            "Dán văn bản tiếng Trung vào đây..."
        )

        layout.addWidget(self.content_edit)

    @property
    def text(self):
        return self.content_edit.toPlainText()

    def set_text(self, value):
        self.content_edit.setPlainText(value)