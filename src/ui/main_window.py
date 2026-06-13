from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QSpinBox,
    QGroupBox,
    QLineEdit,
    QFileDialog,
)

from src.datas.usersetting import UserSettings
from src.services.generate import generate_chinese_practice_sheet


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chinese Character Practice Sheet Generator")
        self.resize(800, 650)

        # Initialize user settings
        self.user_settings = UserSettings()

        self.build_ui()
        self.load_settings()

    def build_ui(self):
        # 1. Main Layout Configuration
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # 2. Text Input Area
        input_label = QLabel("Enter Characters / Content:")
        input_label.setObjectName("HeaderLabel")
        main_layout.addWidget(input_label)

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText(
            "Paste your Chinese text here to generate rows..."
        )
        main_layout.addWidget(self.content_edit)

        # 3. Settings Group Box (Clean Grid Layout, no sub-layouts)
        settings_group = QGroupBox("Configuration Settings")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(12)
        settings_layout.setContentsMargins(16, 20, 16, 16)

        # Row 0: Grid Size & Trace Columns
        settings_layout.addWidget(QLabel("Grid Size:"), 0, 0)
        self.grid_size_spin = QSpinBox()
        self.grid_size_spin.setMinimum(1)
        self.grid_size_spin.setMaximum(200)
        settings_layout.addWidget(self.grid_size_spin, 0, 1)

        settings_layout.addWidget(QLabel("Trace Columns:"), 0, 2)
        self.trace_columns_spin = QSpinBox()
        self.trace_columns_spin.setMinimum(1)
        self.trace_columns_spin.setMaximum(50)
        settings_layout.addWidget(self.trace_columns_spin, 0, 3)

        # Row 1: Margins Left & Top
        settings_layout.addWidget(QLabel("Left Margin:"), 1, 0)
        self.margin_left_spin = QSpinBox()
        self.margin_left_spin.setMinimum(0)
        self.margin_left_spin.setMaximum(100)
        settings_layout.addWidget(self.margin_left_spin, 1, 1)

        settings_layout.addWidget(QLabel("Top Margin:"), 1, 2)
        self.margin_top_spin = QSpinBox()
        self.margin_top_spin.setMinimum(0)
        self.margin_top_spin.setMaximum(100)
        settings_layout.addWidget(self.margin_top_spin, 1, 3)

        # Row 2: Checkbox Option spanning across columns
        self.show_pinyin_check = QCheckBox("Include Pinyin Guides Above Characters")
        settings_layout.addWidget(self.show_pinyin_check, 2, 0, 1, 4)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # 4. File Output Block
        io_group = QGroupBox("Output File Options")
        io_layout = QGridLayout()
        io_layout.setSpacing(12)
        io_layout.setContentsMargins(16, 20, 16, 16)

        # Directory Field Row
        io_layout.addWidget(QLabel("Save Directory:"), 0, 0)
        self.directory_edit = QLineEdit()
        self.directory_edit.setPlaceholderText("No directory chosen...")
        self.directory_edit.setReadOnly(True)
        io_layout.addWidget(self.directory_edit, 0, 1)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setObjectName("SecondaryButton")  # Maps directly to your QSS
        self.browse_btn.clicked.connect(self.choose_directory)
        io_layout.addWidget(self.browse_btn, 0, 2)

        # Filename Field Row
        io_layout.addWidget(QLabel("File Name:"), 1, 0)
        self.filename_edit = QLineEdit()
        self.filename_edit.setPlaceholderText("e.g., worksheet.pdf")
        io_layout.addWidget(self.filename_edit, 1, 1, 1, 2)

        io_group.setLayout(io_layout)
        main_layout.addWidget(io_group)

        # 5. Primary Action Button
        self.generate_btn = QPushButton("Generate PDF Worksheet")
        self.generate_btn.setObjectName(
            "PrimaryButton"
        )  # Activates your gradient styling
        self.generate_btn.clicked.connect(self.generate)
        main_layout.addWidget(self.generate_btn)

        self.setLayout(main_layout)

    def generate(self):
        self.save_settings()
        content = self.content_edit.toPlainText()

        if not self.user_settings.output_directory:
            self.user_settings.output_directory = os.getcwd()

        generate_chinese_practice_sheet(
            characters=content, user_settings=self.user_settings
        )

    def load_settings(self):
        self.grid_size_spin.setValue(self.user_settings.grid_size)
        self.trace_columns_spin.setValue(self.user_settings.trace_columns)
        self.show_pinyin_check.setChecked(self.user_settings.show_pinyin)
        self.margin_left_spin.setValue(self.user_settings.margin_left)
        self.margin_top_spin.setValue(self.user_settings.margin_top)
        self.directory_edit.setText(self.user_settings.output_directory)
        self.filename_edit.setText(self.user_settings.output_filename)

    def save_settings(self):
        self.user_settings.grid_size = self.grid_size_spin.value()
        self.user_settings.trace_columns = self.trace_columns_spin.value()
        self.user_settings.show_pinyin = self.show_pinyin_check.isChecked()
        self.user_settings.margin_left = self.margin_left_spin.value()
        self.user_settings.margin_top = self.margin_top_spin.value()
        self.user_settings.output_directory = self.directory_edit.text()
        self.user_settings.output_filename = self.filename_edit.text()

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Choose Output Directory", ""
        )
        if directory:
            self.directory_edit.setText(directory)
