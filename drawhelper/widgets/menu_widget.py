from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QColor, QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QColorDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from widgets.drawing_widget import DrawingWidget


class MenuWidget(QTabWidget):
    def __init__(self, draw_area):
        super().__init__()
        self.draw_area: DrawingWidget = draw_area
        self.setFixedSize(270, 185)
        self.setStyleSheet(
            """
                font-weight: bold;
                font-size: 13px;
                background-color: rgba(10, 10, 10, 70);
            """,
        )

        # Tab0 - Settings
        tab0 = QWidget()
        tab0_layout = QVBoxLayout()

        # Tab0 - Background
        opacity_changer = QWidget()
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Background:"))
        slider1 = QSlider(Qt.Orientation.Horizontal)
        slider1.valueChanged.connect(self.change_opacity)
        opacity_layout.addWidget(slider1)
        opacity_changer.setLayout(opacity_layout)

        # Tab0 - Exit from app
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_app)

        # Register Tab 1 widgets
        tab0_layout.addWidget(opacity_changer)
        tab0_layout.addWidget(exit_button)
        tab0.setLayout(tab0_layout)

        # Tab 1 - Clear
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QPushButton("Your screen was cleaned!"))
        tab1.setLayout(tab1_layout)
        self.tabBarClicked.connect(self.clear)

        # Tab 2 - Size and drawing modes
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()

        tab2_layout.addWidget(QLabel("Size:"))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self.change_size)
        tab2_layout.addWidget(slider)

        # Tab2 - mode buttons
        buttons = QWidget()
        buttons_layout = QHBoxLayout()

        column1 = QWidget()
        column1_layout = QVBoxLayout()
        circle_button = QPushButton("Circle")
        circle_button.clicked.connect(lambda: self.draw_mode_change("circle"))
        line_button = QPushButton("Line")
        line_button.clicked.connect(lambda: self.draw_mode_change("line"))
        column1_layout.addWidget(circle_button)
        column1_layout.addWidget(line_button)
        column1.setLayout(column1_layout)

        column2 = QWidget()
        column2_layout = QVBoxLayout()
        pen_button = QPushButton("Pen")
        pen_button.clicked.connect(lambda: self.draw_mode_change("pen"))
        column2_layout.addWidget(pen_button)
        column2.setLayout(column2_layout)

        column3 = QWidget()
        column3_layout = QVBoxLayout()
        eraser_button = QPushButton("Eraser")
        eraser_button.clicked.connect(lambda: self.draw_mode_change("eraser"))
        column3_layout.addWidget(eraser_button)
        column3.setLayout(column3_layout)

        buttons_layout.addWidget(column1)
        buttons_layout.addWidget(column2)
        buttons_layout.addWidget(column3)
        buttons.setLayout(buttons_layout)
        tab2_layout.addWidget(buttons)
        tab2.setLayout(tab2_layout)

        # Tab 3 - Color
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QPushButton("Yahoo! You changed color!"))
        tab3.setLayout(tab3_layout)
        self.tabBarClicked.connect(self.choose_color)

        # Add tabs to QTabWidget
        self.addTab(tab0, "Settings")
        self.addTab(tab1, "Clear")
        self.addTab(tab3, "Color")
        self.addTab(tab2, " Modes ")

    # func which is clear drawings
    def clear(self, index):
        if index == 1:
            self.draw_area.image.fill(Qt.GlobalColor.transparent)
            self.draw_area.update()

    # func which is help choose color
    def choose_color(self, index):
        if index == 2:
            color = QColorDialog.getColor()
            if color.isValid():
                self.draw_area.currect_pen.setColor(color)

    # func which is change size of the pen
    def change_size(self, value):
        self.draw_area.currect_pen.setWidthF(value)

    # func which is change background opacity
    def change_opacity(self, value):
        self.draw_area.background_opacity = int(value * 2.5)
        if self.draw_area.background_opacity == 0:
            self.draw_area.background_opacity = 1

        self.draw_area.background.fill(
            QColor(0, 0, 0, self.draw_area.background_opacity),
        )
        self.draw_area.update()

    # the func for exit from the app
    def exit_app(self):
        event = QKeyEvent(
            QEvent.Type.KeyPress,
            Qt.Key.Key_Escape,
            Qt.KeyboardModifier.NoModifier,
        )
        QApplication.postEvent(self, event)

    # change drawing modes
    def draw_mode_change(self, mode):
        self.draw_area.pen.mode = mode
