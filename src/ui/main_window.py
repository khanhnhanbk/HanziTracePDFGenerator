# ui/main_window.py
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)

from src.datas.usersetting import UserSettings, SeparatorEnum
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

        self._sep_options = [
            SeparatorEnum.ANY,
            SeparatorEnum.ENTER,
            SeparatorEnum.COMMA,
            SeparatorEnum.SEMICOLON,
        ]

        self.connect_signals()
        self.load_settings()

    # =========================
    # INIT / SYNC
    # =========================

    def connect_signals(self):
        # Actions
        self.action_panel.normalize_btn.clicked.connect(self.handle_normalize)
        self.action_panel.generate_btn.clicked.connect(self.handle_generate)

        # Browse output
        self.output_panel.browse_btn.clicked.connect(self.handle_browse)

        # Settings sync (UI -> model)
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

        self.settings_panel.multi_char_check.toggled.connect(
            self.on_multi_char_changed
        )

        self.settings_panel.allow_duplicate_check.toggled.connect(
            lambda v: setattr(self.user_settings, "allow_duplicate", bool(v))
        )

        self.settings_panel.separator_combo.currentIndexChanged.connect(
            lambda i: setattr(self.user_settings, "separator", self._sep_options[i])
        )

    # =========================
    # LOAD SETTINGS
    # =========================

    def load_settings(self):
        self.settings_panel.grid_size_spin.setValue(self.user_settings.grid_size)
        self.settings_panel.trace_columns_spin.setValue(self.user_settings.trace_columns)

        self.settings_panel.margin_left_spin.setValue(self.user_settings.margin_left)
        self.settings_panel.margin_top_spin.setValue(self.user_settings.margin_top)

        self.settings_panel.show_pinyin_check.setChecked(self.user_settings.show_pinyin)
        self.settings_panel.allow_duplicate_check.setChecked(self.user_settings.allow_duplicate)

        # IMPORTANT: set first, then sync UI
        self.settings_panel.multi_char_check.setChecked(self.user_settings.multi_char_line)
        self.sync_multi_char_state()

        # separator index
        try:
            idx = self._sep_options.index(self.user_settings.separator)
        except ValueError:
            idx = 0

        self.settings_panel.separator_combo.setCurrentIndex(idx)

        self.output_panel.directory_edit.setText(self.user_settings.output_directory)
        self.output_panel.filename_edit.setText(self.user_settings.output_filename)

        try:
            self.settings_panel.update_page_info()
        except Exception:
            pass

    # =========================
    # SYNC LOGIC (IMPORTANT FIX)
    # =========================

    def sync_multi_char_state(self):
        checked = self.settings_panel.multi_char_check.isChecked()

        # disable separator when multi-char mode is off, enable when on
        self.settings_panel.separator_combo.setDisabled(not checked)

        # auto fix value when locked
        if not checked:
            self.user_settings.separator = SeparatorEnum.COMMA
            idx = self._sep_options.index(SeparatorEnum.COMMA)
            self.settings_panel.separator_combo.setCurrentIndex(idx)

    def on_multi_char_changed(self, checked: bool):
        self.user_settings.multi_char_line = checked
        self.sync_multi_char_state()

    # =========================
    # ACTIONS
    # =========================

    def handle_normalize(self):
        from src.services.normalize import normalizer

        raw = self.content_panel.text
        self.content_panel.set_text(normalizer(raw, self.user_settings))

    def handle_browse(self):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục",
            self.user_settings.output_directory or "",
        )
        if directory:
            self.output_panel.directory_edit.setText(directory)
            self.user_settings.output_directory = directory

    def handle_generate(self):
        filename = self.output_panel.filename_edit.text().strip()
        if filename:
            self.user_settings.output_filename = filename

        characters = self.content_panel.text

        try:
            from src.services.generate import ChinesePracticeSheetGenerator

            ChinesePracticeSheetGenerator(
                characters=characters,
                user_settings=self.user_settings,
            ).generate()

            QMessageBox.information(
                self,
                "Hoàn tất",
                "Tạo PDF thành công:\n"
                + str(
                    Path(self.user_settings.output_directory)
                    / self.user_settings.output_filename
                ),
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Lỗi",
                "Tạo PDF thất bại:\n" + str(exc),
            )

    # =========================
    # SAVE SETTINGS
    # =========================

    def save_settings(self):
        self.user_settings.grid_size = self.settings_panel.grid_size_spin.value()
        self.user_settings.trace_columns = self.settings_panel.trace_columns_spin.value()

        self.user_settings.show_pinyin = self.settings_panel.show_pinyin_check.isChecked()
        self.user_settings.multi_char_line = self.settings_panel.multi_char_check.isChecked()

        sep_idx = self.settings_panel.separator_combo.currentIndex()
        try:
            self.user_settings.separator = self._sep_options[sep_idx]
        except Exception:
            self.user_settings.separator = SeparatorEnum.ENTER

        self.user_settings.allow_duplicate = self.settings_panel.allow_duplicate_check.isChecked()
        self.user_settings.margin_left = self.settings_panel.margin_left_spin.value()
        self.user_settings.margin_top = self.settings_panel.margin_top_spin.value()

        self.user_settings.output_directory = self.output_panel.directory_edit.text()
        self.user_settings.output_filename = self.output_panel.filename_edit.text()

    # =========================
    # PAGE INFO (optional safe call)
    # =========================

    def update_page_info_safe(self):
        try:
            self.settings_panel.update_page_info()
        except Exception:
            pass