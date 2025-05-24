from PyQt6.QtCore import QBuffer, QByteArray, QIODevice
from PyQt6.QtGui import QImage


def qimage_to_bytes(image: QImage) -> bytes:
    ba = QByteArray()
    buffer = QBuffer(ba)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return bytes(ba)


def bytes_to_qimage(data: bytes) -> QImage:
    image = QImage()
    image.loadFromData(data, "PNG")
    return image
