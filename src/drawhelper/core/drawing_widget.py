from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QMouseEvent, QImage, QColor
from PyQt6.QtCore import Qt, QPoint

from drawhelper.utils.qimage_convert import qimage_to_bytes, bytes_to_qimage


# widget which is works as area where user draw
class DrawingWidget(QWidget):
    MAX_HISTORY = 50

    def __init__(self, width, height):
        super().__init__()

        self.pen = QPen(
            Qt.GlobalColor.white,
            5.75,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
        self.eraser = QPen(
            Qt.GlobalColor.transparent,
            5.75,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
        self.pen.mode = "pen"
        self.drawing = False
        self.currect_pen = self.pen

        self.temp_image: QImage = None
        self.setAttribute(Qt.WidgetAttribute.WA_StaticContents)
        self.end_point = QPoint()
        self.start_point = QPoint()

        self.canvas_size = width, height - 50
        self.setFixedSize(*self.canvas_size)

        self.background = QImage(*self.canvas_size,
                                 QImage.Format.Format_ARGB32)
        self.background_opacity = 100
        self.background.fill(QColor(0, 0, 0, self.background_opacity))

        self.image = QImage(*self.canvas_size, QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.transparent)

        self.undo_stack: list[bytes] = []
        self.redo_stack: list[bytes] = []

    # funcs for drawing
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.pen.mode in ('pen', "eraser"):
                self.drawing = True
                self.end_point = event.position().toPoint()
                self.save_history(self.image)
            elif self.pen.mode in ('circle', 'line'):
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
                self.currect_pen = self.pen
                painter.setPen(self.pen)
                current_point = event.position().toPoint()
                painter.drawLine(self.end_point, current_point)
                self.end_point = current_point

            if self.pen.mode == 'circle':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                self.currect_pen = self.pen
                painter.setPen(self.pen)
                current_point = event.position().toPoint()
                radius = (self.start_point - current_point).manhattanLength()
                painter.drawEllipse(self.start_point, radius, radius)

            if self.pen.mode == 'line':
                self.temp_image = self.image.copy()
                painter = QPainter(self.temp_image)
                self.currect_pen = self.pen
                painter.setPen(self.pen)
                painter.drawLine(self.start_point, event.position().toPoint())

            if self.pen.mode == "eraser":
                painter = QPainter(self.image)
                painter.setCompositionMode(
                    QPainter.CompositionMode.CompositionMode_Clear
                    )
                self.currect_pen = self.eraser
                painter.setPen(self.eraser)
                current_point = event.position().toPoint()
                painter.drawLine(self.end_point, current_point)
                self.end_point = current_point

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
        image_bytes = qimage_to_bytes(image)
        self.undo_stack.append(image_bytes)
        if len(self.undo_stack) > self.MAX_HISTORY:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(qimage_to_bytes(self.image))
            self.image = bytes_to_qimage(self.undo_stack.pop())
            self.update()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(qimage_to_bytes(self.image))
            self.image = bytes_to_qimage(self.redo_stack.pop())
            self.update()
