from PyQt6.QtWidgets import QApplication

from drawhelper.core.main_window import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
