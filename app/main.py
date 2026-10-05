import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow


def load_stylesheet():
    stylesheet_path = (
        Path(__file__).parent / "ui" / "style.qss"
    )

    return stylesheet_path.read_text(encoding="utf-8")


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()