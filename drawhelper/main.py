from PyQt6.QtWidgets import QApplication

from widgets.main_widget import MainWidget


def main():
    app = QApplication([])
    window = MainWidget()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
