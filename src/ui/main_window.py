# ui/main_window.py
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)

from src.datas.usersetting import UserSettings
from src.ui.widgets.action_panel import ActionPanel
from src.ui.widgets.content_panel import ContentPanel
from src.ui.widgets.output_panel import OutputPanel
from src.ui.widgets.settings_panel import SettingsPanel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trình tạo phiếu luyện viết chữ Hán")
        self.resize(800, 650)

        self.user_settings = UserSettings()

        self.content_panel = ContentPanel()
        self.settings_panel = SettingsPanel()
        self.output_panel = OutputPanel()
        self.action_panel = ActionPanel()

        layout = QVBoxLayout(self)

        layout.addWidget(self.content_panel)
        layout.addWidget(self.settings_panel)
        layout.addWidget(self.output_panel)
        layout.addWidget(self.action_panel)

        self.connect_signals()
        self.load_settings()

    def connect_signals(self):
        # Initialize widget values from user settings
        self.settings_panel.grid_size_spin.setValue(self.user_settings.grid_size)
        self.settings_panel.trace_columns_spin.setValue(
            self.user_settings.trace_columns
        )
        self.settings_panel.margin_left_spin.setValue(self.user_settings.margin_left)
        self.settings_panel.margin_top_spin.setValue(self.user_settings.margin_top)
        self.settings_panel.show_pinyin_check.setChecked(self.user_settings.show_pinyin)

        self.output_panel.directory_edit.setText(self.user_settings.output_directory)
        self.output_panel.filename_edit.setText(self.user_settings.output_filename)

        # Actions
        self.action_panel.normalize_btn.clicked.connect(self.handle_normalize)
        self.action_panel.generate_btn.clicked.connect(self.handle_generate)

        # Output browse
        self.output_panel.browse_btn.clicked.connect(self.handle_browse)

        # Sync settings widgets back to user_settings
        self.settings_panel.grid_size_spin.valueChanged.connect(
            lambda v: setattr(self.user_settings, "grid_size", v)
        )
        self.settings_panel.trace_columns_spin.valueChanged.connect(
            lambda v: setattr(self.user_settings, "trace_columns", v)
        )
        self.settings_panel.margin_left_spin.valueChanged.connect(
            lambda v: setattr(self.user_settings, "margin_left", v)
        )
        self.settings_panel.margin_top_spin.valueChanged.connect(
            lambda v: setattr(self.user_settings, "margin_top", v)
        )
        self.settings_panel.show_pinyin_check.toggled.connect(
            lambda v: setattr(self.user_settings, "show_pinyin", bool(v))
        )

    def handle_normalize(self):
        from src.services.normalize import normalizer

        raw = self.content_panel.text
        normalized = normalizer(raw)
        self.content_panel.set_text(normalized)

    def handle_browse(self):
        directory = QFileDialog.getExistingDirectory(self, "Chọn thư mục", self.user_settings.output_directory or "")
        if directory:
            self.output_panel.directory_edit.setText(directory)
            self.user_settings.output_directory = directory
    def handle_generate(self):
        # Update filename from UI
        filename = self.output_panel.filename_edit.text().strip()
        if filename:
            self.user_settings.output_filename = filename

        # persist settings
        self.save_settings()

        characters = self.content_panel.text

        if not self.user_settings.output_directory:
            self.user_settings.output_directory = os.getcwd()

        try:
            from src.services.generate import generate_chinese_practice_sheet

            generate_chinese_practice_sheet(
                characters=characters, user_settings=self.user_settings
            )
            QMessageBox.information(
                self,
                "Hoàn tất",
                "Tạo PDF thành công. Tệp đã được lưu vào:\n" +
                str(Path(self.user_settings.output_directory) / self.user_settings.output_filename),
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Lỗi",
                "Tạo PDF thất bại:\n" + str(exc),
            )

    def load_settings(self):
        self.settings_panel.grid_size_spin.setValue(self.user_settings.grid_size)
        self.settings_panel.trace_columns_spin.setValue(self.user_settings.trace_columns)
        self.settings_panel.show_pinyin_check.setChecked(self.user_settings.show_pinyin)
        self.settings_panel.margin_left_spin.setValue(self.user_settings.margin_left)
        self.settings_panel.margin_top_spin.setValue(self.user_settings.margin_top)
        self.output_panel.directory_edit.setText(self.user_settings.output_directory)
        self.output_panel.filename_edit.setText(self.user_settings.output_filename)
        # ensure page info is updated in settings panel
        try:
            self.settings_panel.update_page_info()
        except Exception:
            pass

    def save_settings(self):
        self.user_settings.grid_size = self.settings_panel.grid_size_spin.value()
        self.user_settings.trace_columns = self.settings_panel.trace_columns_spin.value()
        self.user_settings.show_pinyin = self.settings_panel.show_pinyin_check.isChecked()
        self.user_settings.margin_left = self.settings_panel.margin_left_spin.value()
        self.user_settings.margin_top = self.settings_panel.margin_top_spin.value()
        self.user_settings.output_directory = self.output_panel.directory_edit.text()
        self.user_settings.output_filename = self.output_panel.filename_edit.text()