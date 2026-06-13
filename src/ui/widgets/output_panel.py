# ui/widgets/output_panel.py

from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class OutputPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        group = QGroupBox("Tùy chọn tệp đầu ra")
        grid = QGridLayout(group)

        self.directory_edit = QLineEdit()
        self.directory_edit.setReadOnly(True)
        self.directory_edit.setPlaceholderText("Chưa chọn thư mục...")

        self.filename_edit = QLineEdit()

        self.browse_btn = QPushButton("Chọn...")
        self.browse_btn.setObjectName("SecondaryButton")

        grid.addWidget(QLabel("Thư mục"), 0, 0)
        grid.addWidget(self.directory_edit, 0, 1)
        grid.addWidget(self.browse_btn, 0, 2)

        grid.addWidget(QLabel("Tên tệp"), 1, 0)
        grid.addWidget(self.filename_edit, 1, 1, 1, 2)

        layout.addWidget(group)