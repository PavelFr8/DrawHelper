from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QSettings, Qt
from PyQt6.QtGui import QColor, QKeyEvent, QKeySequence
from PyQt6.QtWidgets import QErrorMessage, QHBoxLayout, QMainWindow, QWidget

from utils.get_screen_size import get_screen_size
from widgets.drawing_widget import DrawingWidget
from widgets.menu_widget import MenuWidget


class MainWidget(QMainWindow):
    DEFAULT_SAVE_PATH = "saves"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DrawHelper")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.window_size = get_screen_size()
        self.setGeometry(1, 1, *self.window_size)

        central_widget = QWidget(self)
        central_layout = QHBoxLayout(central_widget)
        self.drawing_widget = DrawingWidget(*self.window_size)
        central_layout.addWidget(self.drawing_widget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        self.menu_widget = MenuWidget(self.drawing_widget)
        self.menu_widget.setParent(self)
        self.menu_widget.setGeometry(1, 1, 200, self.window_size[1] - 50)

        self.settings = QSettings("DrawHelperOrg", "DrawHelperApp")
        self.load_save()

    # Function to close the app
    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        match key:
            case Qt.Key.Key_Escape:
                self.create_save()
                self.close()
            case Qt.Key.Key_P:
                self.drawing_widget.pen.mode = "pen"
            case Qt.Key.Key_E:
                self.drawing_widget.pen.mode = "eraser"
            case Qt.Key.Key_L:
                self.drawing_widget.pen.mode = "line"
            case Qt.Key.Key_C:
                self.drawing_widget.pen.mode = "circle"
            case _:
                super().keyPressEvent(event)

        if event.matches(QKeySequence.StandardKey.Undo):  # Ctrl+Z
            self.drawing_widget.undo()

        if event.matches(QKeySequence.StandardKey.Redo):  # Ctrl+Y
            self.drawing_widget.redo()

        if event.matches(QKeySequence.StandardKey.Save):  # Ctrl+S
            self.create_save()

    def load_save(self):
        try:
            color = self.settings.value("pen_color", "#FFFFFF")
            size = float(self.settings.value("pen_size", 5.0))
            opacity = int(self.settings.value("background_opacity", 100))

            self.drawing_widget.pen.setColor(QColor(color))
            self.drawing_widget.pen.setWidthF(size)
            self.drawing_widget.background_opacity = opacity
            self.drawing_widget.background.fill(QColor(0, 0, 0, opacity))

            image_data = self.settings.value("image_data", QByteArray())
            if image_data and not image_data.isEmpty():
                self.drawing_widget.image.loadFromData(image_data, "PNG")

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(f"Failed to load settings: {str(e)}")

    def create_save(self):
        try:
            self.settings.setValue(
                "pen_color",
                self.drawing_widget.pen.color().name(),
            )
            self.settings.setValue(
                "pen_size",
                self.drawing_widget.pen.widthF(),
            )
            self.settings.setValue(
                "background_opacity",
                self.drawing_widget.background_opacity,
            )

            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            self.drawing_widget.image.save(buffer, "PNG")
            self.settings.setValue("image_data", buffer.data())

            self.settings.sync()

        except Exception as e:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage(f"Failed to save data: {str(e)}")
