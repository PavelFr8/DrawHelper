import os.path

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QHBoxLayout, QLabel, QSlider, QColorDialog, QPushButton, QVBoxLayout
from PyQt6.QtGui import QPainter, QPen, QMouseEvent, QImage, QKeyEvent, QColor
from PyQt6.QtCore import Qt, QPoint, QSize

from funcs.create_save import create_save
from funcs.get_save import get_save
from funcs.get_screen_size import get_screen_size

import sys


w, h = get_screen_size()

# widget which is works as area where user draw
class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.drawing = False
        self.last_point = QPoint()
        self.start_point = QPoint()
        self.temp_image = None
        self.setFixedSize(w, h)
        self.mode = 'pen'

        # load save data
        data = get_save()
        print(data)
        self.paint_size = data['size']
        self.color = QColor(data['color'])
        self.opacity = data['opacity']
        if os.path.exists('saves/save.png'):
            self.image = QImage('saves/save.png')
        else:
            self.image = QImage(QSize(w, h - 50), QImage.Format.Format_ARGB32)
            self.image.fill(QColor(0, 0, 0, 100))

    # next funcs for drawing
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.mode == 'pen':
                self.drawing = True
                self.last_point = event.position().toPoint()
            elif self.mode == 'circle' or self.mode == 'line':
                if not self.drawing:
                    self.drawing = True
                    self.start_point = event.position().toPoint()
                    self.temp_image = self.image.copy()
                else:
                    self.drawing = False
                    self.image = self.temp_image
                    self.update()


    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            if self.mode == 'pen':
                painter = QPainter(self.image)
                painter.setPen(QPen(self.color, self.paint_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                current_point = event.position().toPoint()
                painter.drawLine(self.last_point, current_point)
                self.last_point = current_point
                self.update()

            elif self.mode == 'circle':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                painter.setPen(QPen(self.color, self.paint_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                current_point = event.position().toPoint()
                radius = (self.start_point - current_point).manhattanLength()
                painter.drawEllipse(self.start_point, radius, radius)
                self.update()

            elif self.mode == 'line':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                painter.setPen(QPen(self.color, self.paint_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                    Qt.PenJoinStyle.RoundJoin))
                painter.drawLine(self.start_point, event.position().toPoint())
                self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            if self.mode == 'circle':
                self.image = self.temp_image
            if self.mode == 'line':
                self.image = self.temp_image
                self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        if self.temp_image and (self.mode == 'circle' or self.mode == 'line') and self.drawing:
            canvas_painter.drawImage(0, 0, self.temp_image)
        else:
            canvas_painter.drawImage(0, 0, self.image)


# the menu class
class MenuWidget(QTabWidget):
    def __init__(self, draw_area):
        super().__init__()
        self.draw_area = draw_area
        self.setFixedSize(260, 115)
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

        # Tab 2 - Size
        tab2 = QWidget()
        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(QLabel('Size:'))

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self.change_size)
        tab2_layout.addWidget(slider)

        buttons = QWidget()
        buttons_layout = QVBoxLayout()

        circle_button = QPushButton('Circle')
        circle_button.clicked.connect(lambda: self.draw_mode_change('circle'))
        line_button = QPushButton('Line')
        line_button.clicked.connect(lambda: self.draw_mode_change('line'))
        pen_button = QPushButton('Pen')
        pen_button.clicked.connect(lambda: self.draw_mode_change('pen'))

        buttons_layout.addWidget(circle_button)
        buttons_layout.addWidget(line_button)
        buttons_layout.addWidget(pen_button)
        buttons.setLayout(buttons_layout)
        tab2_layout.addWidget(buttons)

        tab2.setLayout(tab2_layout)

        # Tab 3 - Color
        tab3 = QWidget()
        self.tabBarClicked.connect(self.choose_color)

        # Add tabs to QTabWidget
        self.addTab(tab0, "Settings")
        self.addTab(tab1, "Clear")
        self.addTab(tab3, "Color")
        self.addTab(tab2, " Modes ")

    # func which is clear drawings
    def clear(self, index):
        if index == 1:
            # print('clear')
            self.draw_area.image.fill(QColor(0, 0, 0, self.draw_area.opacity))
            self.draw_area.update()
            print(self.draw_area.opacity)

    # func which is help choose color
    def choose_color(self, index):
        if index == 2:
            self.draw_area.color = QColorDialog.getColor()

    # func which is change size of the pen
    def change_size(self, value):
        self.draw_area.paint_size = value / 4

    # func which is change background opacity
    def change_opacity(self, value):
        self.draw_area.opacity = int(value * 2.5)
        if self.draw_area.opacity == 0:
            self.draw_area.opacity = 1
        self.draw_area.image.fill(QColor(0, 0, 0, self.draw_area.opacity))
        self.draw_area.update()

    # the func for exit from the app
    def exit(self):
        create_save(self.draw_area)
        sys.exit(app.exec())

    # change drawing modes
    def draw_mode_change(self, mode):
        self.draw_area.mode = mode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DrawHelper")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(1, 1, w, h - 50)

        # add drawing area
        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        self.drawing_widget = DrawingWidget()
        central_layout.addWidget(self.drawing_widget)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        # add menu
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
