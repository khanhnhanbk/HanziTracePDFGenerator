from PySide6.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from services.generate import generate_chinese_practice_sheet


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Content Generator")
        self.resize(800, 600)

        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout()

        # Text area
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText(
            "Paste content here..."
        )

        main_layout.addWidget(self.content_edit)

        # Options
        self.option_a = QCheckBox("Option A")
        self.option_b = QCheckBox("Option B")

        main_layout.addWidget(self.option_a)
        main_layout.addWidget(self.option_b)

        # Language dropdown
        lang_layout = QHBoxLayout()

        lang_layout.addWidget(QLabel("Language:"))

        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English",
            "Chinese",
            "Vietnamese"
        ])

        lang_layout.addWidget(self.language_combo)

        main_layout.addLayout(lang_layout)

        # Output dropdown
        output_layout = QHBoxLayout()

        output_layout.addWidget(QLabel("Output:"))

        self.output_combo = QComboBox()
        self.output_combo.addItems([
            "CSV",
            "Excel",
            "TXT"
        ])

        output_layout.addWidget(self.output_combo)

        main_layout.addLayout(output_layout)

        # Generate button
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(
            self.generate
        )

        main_layout.addWidget(self.generate_btn)

        self.setLayout(main_layout)

    def generate(self):
        content = self.content_edit.toPlainText()
        generate_chinese_practice_sheet(filename="output.pdf", characters=content)