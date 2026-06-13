import sys
import os
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication
)

from src.ui.main_window import MainWindow

# Handle both normal runs and PyInstaller bundled exe
if getattr(sys, 'frozen', False):
    # Running as PyInstaller exe
    base_path = Path(sys._MEIPASS)
else:
    # Running as normal Python script
    base_path = Path(__file__).parent

qss_file = base_path / "styles" / "main.qss"


def create_app():
    """Create and configure the QApplication"""
    app = QApplication(sys.argv)
    with open(qss_file, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    return app


def main():
    """Main entry point"""
    app = create_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
