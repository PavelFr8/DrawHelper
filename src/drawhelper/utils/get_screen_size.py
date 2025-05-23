from PyQt6.QtGui import QGuiApplication


def get_screen_size() -> tuple[int, int]:
    screen = QGuiApplication.primaryScreen()
    geometry = screen.geometry()
    dpr = screen.devicePixelRatio()

    width = int(geometry.width() * dpr)
    height = int(geometry.height() * dpr)
    return width, height
