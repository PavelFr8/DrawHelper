import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QHBoxLayout, QLabel, QSlider, QColorDialog, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QMouseEvent, QImage, QKeyEvent, QColor
from PyQt6.QtCore import Qt, QPoint, QSize
from funcs.create_save import create_save
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
        self.paint_size = 10
        self.color = QColor('#000000')
        self.opacity = 50
        self.last_point = QPoint()
        self.image = QImage(QSize(w, h - 50), QImage.Format.Format_ARGB32)
        self.image.fill(QColor(0, 0, 0, self.opacity))
        self.setFixedSize(w, h)

    # next funcs for drawing
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.color, self.paint_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(0, 0, self.image)


# the menu class
class MenuWidget(QTabWidget):
    def __init__(self, draw_area):
        super().__init__()
        self.draw_area = draw_area
        self.setFixedSize(288, 115)
        self.setStyleSheet("""
            font-weight: bold;
            font-size: 13px;
            background-color: rgba(10, 10, 10, 30);
        """)

        # Tab0 - Settings
        tab0 = QWidget()
        tab0_layout = QVBoxLayout()

        opacity_changer = QWidget()
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel('Background:'))
        slider1 = QSlider(Qt.Orientation.Horizontal)
        slider1.valueChanged.connect(self.change_opacity)
        opacity_layout.addWidget(slider1)
        opacity_changer.setLayout(opacity_layout)

        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.exit)

        tab0_layout.addWidget(opacity_changer)
        tab0_layout.addWidget(exit_button)
        tab0.setLayout(tab0_layout)

        # Tab 1 - Clear
        tab1 = QWidget()
        self.tabBarClicked.connect(self.clear)

        # Tab 2 - Color
        tab2 = QWidget()
        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(QLabel('Size:'))

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self.change_size)
        tab2_layout.addWidget(slider)

        tab2.setLayout(tab2_layout)

        # Tab 3 - Size
        tab3 = QWidget()
        self.tabBarClicked.connect(self.choose_color)

        # Add tabs to QTabWidget
        self.addTab(tab0, "Settings")
        self.addTab(tab1, "Clear")
        self.addTab(tab3, "Color")
        self.addTab(tab2, " Size ")

    # func which is clear drawings
    def clear(self, index):
        if index == 1:
            # print('clear')
            self.draw_area.image.fill(QColor(0, 0, 0, self.draw_area.opacity))
            self.draw_area.update()

    # func which is help choose color
    def choose_color(self, index):
        if index == 2:
            self.draw_area.color = QColorDialog.getColor()

    # func which is change size of the pen
    def change_size(self, value):
        self.draw_area.paint_size = value / 4

    def change_opacity(self, value):
        self.draw_area.opacity = int(value * 2.5)
        if self.draw_area.opacity == 0:
            self.draw_area.opacity = 1
        self.draw_area.image.fill(QColor(0, 0, 0, self.draw_area.opacity))
        self.draw_area.update()

    def exit(self):
        create_save(self.draw_area)
        sys.exit(app.exec())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DrawHelper")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(1, 1, w, h - 50)

        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        self.drawing_widget = DrawingWidget()
        central_layout.addWidget(self.drawing_widget)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        self.menu_widget = MenuWidget(self.drawing_widget)
        self.menu_widget.setParent(self)
        self.menu_widget.setGeometry(1, 1, 200, h - 50)

    # Function to close the app
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            create_save(self.drawing_widget)
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
