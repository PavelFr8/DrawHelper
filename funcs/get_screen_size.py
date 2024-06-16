import ctypes


# get the size of users screen.
def get_screen_size():
    user32 = ctypes.windll.user32
    w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return w, h