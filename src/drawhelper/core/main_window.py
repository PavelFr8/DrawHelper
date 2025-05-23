import os.path
import json

from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtGui import QKeyEvent, QColor
from PyQt6.QtCore import Qt

from utils.get_screen_size import get_screen_size

from core.drawing_widget import DrawingWidget
from core.menu_widget import MenuWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.DEFAULT_SAVE_PATH = "saves"

        self.setWindowTitle("DrawHelper")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.window_size = get_screen_size()
        self.setGeometry(1, 1, *self.window_size)

        # add drawing area
        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        self.drawing_widget = DrawingWidget(*self.window_size)
        central_layout.addWidget(self.drawing_widget)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)

        # add menu
        self.menu_widget = MenuWidget(self.drawing_widget)
        self.menu_widget.setParent(self)
        self.menu_widget.setGeometry(1, 1, 200, self.window_size[1] - 50)

        self.load_save()

    # Function to close the app
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.create_save()
            self.close()

        if event.key() == (Qt.Key.Key_Control and Qt.Key.Key_Z):
            if self.drawing_widget.history:
                self.drawing_widget.image = self.drawing_widget.history.pop()
                self.drawing_widget.update()

    def load_save(self):
        try:
            save_path = os.path.join(self.DEFAULT_SAVE_PATH, "save.json")
            with open(save_path) as f:
                data = json.loads(f.read())
            self.drawing_widget.pen.setWidthF(data["size"])
            self.drawing_widget.pen.setColor(QColor(data["color"]))
            self.drawing_widget.background_opacity = data["opacity"]
        except Exception:
            self.drawing_widget.pen.setWidth(10)
            self.drawing_widget.pen.setColor(QColor("#c71d1d"))
            self.drawing_widget.background_opacity = 100

    def create_save(self):
        try:
            os.makedirs(self.DEFAULT_SAVE_PATH, exist_ok=True)
            data = {
                "color": self.drawing_widget.pen.color().name(),
                "size": self.drawing_widget.pen.widthF(),
                "opacity": self.drawing_widget.background_opacity,
            }
            save_path = os.path.join(self.DEFAULT_SAVE_PATH, "save.json")
            self.drawing_widget.image.save(
                os.path.join(self.DEFAULT_SAVE_PATH, "save.png")
            )
            with open(save_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print("Saving error:", e)
