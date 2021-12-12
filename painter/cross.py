import win32gui


def make_cross():
    dc = win32gui.GetDC(0)
    win32gui.MoveToEx(dc, 0, 0)
    win32gui.LineTo(dc, 1920, 1080)
    win32gui.MoveToEx(dc, 1920, 0)
    win32gui.LineTo(dc, 0, 1080)
