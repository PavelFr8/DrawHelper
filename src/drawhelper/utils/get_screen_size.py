import ctypes


# get the size of users screen.
def get_screen_size() -> tuple[int, int]:
    user32 = ctypes.windll.user32
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return width, height
