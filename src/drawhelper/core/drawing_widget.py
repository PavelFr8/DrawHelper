from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QMouseEvent, QImage, QColor
from PyQt6.QtCore import Qt, QPoint, QSize


# widget which is works as area where user draw
class DrawingWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()

        self.pen = QPen(
            QColor("#ffffff"),
            5.75,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
        self.pen.mode = "pen"
        self.drawing = False

        self.temp_image: QImage = None
        self.history = []
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.end_point = QPoint()
        self.start_point = QPoint()

        self.canvas_size = width, height - 50
        self.setFixedSize(*self.canvas_size)

        self.background = QImage(QSize(*self.canvas_size),
                                 QImage.Format.Format_ARGB32)
        self.background_opacity = 100
        self.background.fill(QColor(0, 0, 0, self.background_opacity))

        self.image = QImage(QSize(*self.canvas_size),
                            QImage.Format.Format_ARGB32)
        self.image.fill(QColor(0, 0, 0, 1))

    # funcs for drawing
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.pen.mode == 'pen':
                self.drawing = True
                self.end_point = event.position().toPoint()
                self.save_history(self.image)
            elif self.pen.mode == 'circle' or self.pen.mode == 'line':
                if not self.drawing:
                    self.drawing = True
                    self.start_point = event.position().toPoint()
                    self.temp_image = self.image.copy()
                    self.save_history(self.temp_image)
                    self.update()
                else:
                    self.drawing = False
                    self.image = self.temp_image

    # func for drawing in different drawing modes
    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            if self.pen.mode == 'pen':
                painter = QPainter(self.image)
                painter.setPen(self.pen)
                current_point = event.position().toPoint()
                painter.drawLine(self.end_point, current_point)
                self.end_point = current_point

            elif self.pen.mode == 'circle':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                painter.setPen(self.pen)
                current_point = event.position().toPoint()
                radius = (self.start_point - current_point).manhattanLength()
                painter.drawEllipse(self.start_point, radius, radius)

            elif self.pen.mode == 'line':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                painter.setPen(self.pen)
                painter.drawLine(self.start_point, event.position().toPoint())

            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            if self.pen.mode == "circle" or self.pen.mode == "line":
                self.image = self.temp_image
            self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)

        canvas_painter.drawImage(0, 0, self.background)

        if (
            self.temp_image
            and (self.pen.mode == 'circle' or self.pen.mode == 'line')
            and self.drawing
        ):
            canvas_painter.drawImage(0, 0, self.temp_image)
        else:
            canvas_painter.drawImage(0, 0, self.image)

    def save_history(self, image):
        if len(self.history) >= 10:
            self.history.pop(-1)
        self.history.append(image.copy())
