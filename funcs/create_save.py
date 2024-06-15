from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt6.QtGui import QAction  # Импортируем QAction отсюда

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создаем действие для меню
        exitAction = QAction('&Выход', self)
        exitAction.triggered.connect(self.close)

        # Создаем само меню
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Пример QMenu')
        self.show()

def main():
    app = QApplication([])
    ex = MainWindow()
    app.exec()

if __name__ == '__main__':
    main()