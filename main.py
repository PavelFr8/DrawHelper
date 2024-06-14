import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QHBoxLayout, QPushButton, \
    QLabel
from PyQt6.QtGui import QPainter, QPen, QMouseEvent, QImage, QKeyEvent, QColor
from PyQt6.QtCore import Qt, QPoint, QSize
import ctypes

# get the size of users screen.
user32 = ctypes.windll.user32
w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


# widget which is works as area where user draw
class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.drawing = False
        self.last_point = QPoint()
        self.image = QImage(QSize(w, h - 50), QImage.Format.Format_ARGB32)
        self.image.fill(QColor(0, 0, 0, 100))
        self.setFixedSize(w, h)

    # funcs for drawing
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.GlobalColor.black, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(0, 0, self.image)


# the menu
class MenuWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 100)

        # Tab 1 - Clear
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel("1"))
        tab1.setLayout(tab1_layout)

        # Tab 2 - Color
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("2"))
        tab2.setLayout(tab2_layout)

        # Tab 3 - Size
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QLabel("3"))
        tab3.setLayout(tab3_layout)

        # Add tabs to QTabWidget
        self.addTab(tab1, "  Очистить  ")
        self.addTab(tab2, "    Цвет    ")
        self.addTab(tab3, "   Размер   ")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DrawHelper")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(1, 1, w, h - 50)

        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        drawing_widget = DrawingWidget()
        central_layout.addWidget(drawing_widget)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.menu_widget = MenuWidget()
        self.menu_widget.setParent(self)
        self.menu_widget.setGeometry(1, 1, 200, h - 50)

    # Function to close the app
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
