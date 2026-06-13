# ui/widgets/action_panel.py

from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ActionPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.normalize_btn = QPushButton(
            "Chuẩn hóa văn bản"
        )

        self.normalize_btn.setObjectName("SecondaryButton")

        self.generate_btn = QPushButton(
            "Tạo PDF phiếu luyện"
        )

        self.generate_btn.setObjectName("PrimaryButton")

        layout.addWidget(self.normalize_btn)
        layout.addWidget(self.generate_btn)