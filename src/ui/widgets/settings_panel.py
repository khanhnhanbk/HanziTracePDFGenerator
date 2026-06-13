# ui/widgets/settings_panel.py

from reportlab.lib.pagesizes import A4
from PySide6.QtWidgets import (
    QWidget,
    QGroupBox,
    QGridLayout,
    QLabel,
    QSpinBox,
    QCheckBox,
    QVBoxLayout,
)


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        group = QGroupBox("Cài đặt cấu hình")
        grid = QGridLayout(group)

        self.grid_size_spin = QSpinBox()
        self.trace_columns_spin = QSpinBox()
        self.grid_size_spin.setMinimum(1)
        self.grid_size_spin.setMaximum(200)

        self.trace_columns_spin.setMinimum(1)
        self.trace_columns_spin.setMaximum(50)

        self.margin_left_spin = QSpinBox()
        self.margin_top_spin = QSpinBox()

        self.show_pinyin_check = QCheckBox(
            "Bao gồm chú âm (Pinyin)"
        )

        self.page_info_label = QLabel()
        self.page_info_label.setObjectName("HeaderLabel")

        grid.addWidget(QLabel("Kích thước ô"), 0, 0)
        grid.addWidget(self.grid_size_spin, 0, 1)

        grid.addWidget(QLabel("Số cột mẫu"), 0, 2)
        grid.addWidget(self.trace_columns_spin, 0, 3)

        grid.addWidget(QLabel("Lề trái"), 1, 0)
        grid.addWidget(self.margin_left_spin, 1, 1)

        grid.addWidget(QLabel("Lề trên"), 1, 2)
        grid.addWidget(self.margin_top_spin, 1, 3)

        grid.addWidget(self.page_info_label, 2, 0, 1, 4)
        grid.addWidget(self.show_pinyin_check, 3, 0, 1, 4)

        layout.addWidget(group)

        self.grid_size_spin.valueChanged.connect(
            self.update_page_info
        )
        self.margin_left_spin.valueChanged.connect(
            self.update_page_info
        )
        self.margin_top_spin.valueChanged.connect(
            self.update_page_info
        )

    def update_page_info(self):
        grid_size = self.grid_size_spin.value()
        margin_left = self.margin_left_spin.value()
        margin_top = self.margin_top_spin.value()

        if grid_size <= 0:
            self.page_info_label.setText("Hàng x Cột trên A4: 0 x 0")
            return

        usable_width = A4[0] - margin_left * 2
        usable_height = A4[1] - margin_top * 2
        cols = max(0, int(usable_width // grid_size))
        rows = max(0, int(usable_height // grid_size))

        self.page_info_label.setText(
            f"Hàng x Cột trên A4: {rows} x {cols}"
        )