import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication
)

from ui.main_window import MainWindow

qss_file = Path(__file__).parent / "styles" / "main.qss"


app = QApplication(sys.argv)
with open(qss_file, "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()

sys.exit(app.exec())