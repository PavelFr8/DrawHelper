from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QHBoxLayout, QLabel, QSlider, QColorDialog,
    QPushButton, QVBoxLayout
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from core.drawing_widget import DrawingWidget

import sys


# the menu class
class MenuWidget(QTabWidget):
    def __init__(self, draw_area):
        super().__init__()
        self.draw_area: DrawingWidget = draw_area
        self.setFixedSize(260, 145)
        self.setStyleSheet("""
            font-weight: bold;
            font-size: 13px;
            background-color: rgba(10, 10, 10, 70);
        """)

        # Tab0 - Settings
        tab0 = QWidget()
        tab0_layout = QVBoxLayout()

        # Tab0 - Background
        opacity_changer = QWidget()
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel('Background:'))
        slider1 = QSlider(Qt.Orientation.Horizontal)
        slider1.valueChanged.connect(self.change_opacity)
        opacity_layout.addWidget(slider1)
        opacity_changer.setLayout(opacity_layout)

        # Tab0 - Exit from app
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.exit)

        # Register Tab 1 widgets
        tab0_layout.addWidget(opacity_changer)
        tab0_layout.addWidget(exit_button)
        tab0.setLayout(tab0_layout)

        # Tab 1 - Clear
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QPushButton('Your screen was cleaned!'))
        tab1.setLayout(tab1_layout)
        self.tabBarClicked.connect(self.clear)

        # Tab 2 - Size and drawing modes
        tab2 = QWidget()
        tab2_layout = QHBoxLayout()

        # Tab2 - Size
        tab2_layout.addWidget(QLabel('Size:'))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.valueChanged.connect(self.change_size)
        tab2_layout.addWidget(slider)

        # Tab2 - mode buttons
        buttons = QWidget()
        buttons_layout = QVBoxLayout()

        circle_button = QPushButton('Circle')
        circle_button.clicked.connect(lambda: self.draw_mode_change('circle'))
        line_button = QPushButton('Line')
        line_button.clicked.connect(lambda: self.draw_mode_change('line'))
        pen_button = QPushButton('Pen')
        pen_button.clicked.connect(lambda: self.draw_mode_change('pen'))

        # Register Tab 2 widgets
        buttons_layout.addWidget(circle_button)
        buttons_layout.addWidget(line_button)
        buttons_layout.addWidget(pen_button)
        buttons.setLayout(buttons_layout)
        tab2_layout.addWidget(buttons)
        tab2.setLayout(tab2_layout)

        # Tab 3 - Color
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QPushButton('Yahoo! You changed color!'))
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
            self.draw_area.image.fill(QColor(0, 0, 0, 1))
            self.draw_area.update()

    # func which is help choose color
    def choose_color(self, index):
        if index == 2:
            color = QColorDialog.getColor()
            if color.isValid():
                self.draw_area.pen.setColor(color)

    # func which is change size of the pen
    def change_size(self, value):
        self.draw_area.pen.setWidthF(value / 4)

    # func which is change background opacity
    def change_opacity(self, value):
        self.draw_area.background_opacity = int(value * 2.5)
        if self.draw_area.background_opacity == 0:
            self.draw_area.background_opacity = 1
        self.draw_area.background.fill(
            QColor(0, 0, 0, self.draw_area.background_opacity)
        )
        self.draw_area.update()

    # the func for exit from the app
    def exit(self):
        

    # change drawing modes
    def draw_mode_change(self, mode):
        self.draw_area.mode = mode
