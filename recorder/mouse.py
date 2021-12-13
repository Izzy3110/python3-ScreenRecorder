import threading
import time
import pyautogui
from pynput import mouse


class RecordMousePos(threading.Thread):
    running = True
    current_pos = {
        "x": None,
        "y": None
    }

    def __init__(self):
        super(RecordMousePos, self).__init__()

    def run(self) -> None:
        while self.running:
            self.current_pos["x"], self.current_pos["y"] = pyautogui.position()
            print(self.current_pos)


class MouseMonitor(threading.Thread):
    listener = None
    is_started = False
    running = True
    messages = []

    def __init__(self):

        # Collect events until released
        """
        with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
            listener.join()
        """

        # ...or, in a non-blocking fashion:
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        super(MouseMonitor, self).__init__()

    def run(self) -> None:
        while self.running:
            if not self.is_started:
                self.is_started = True
                self.listener.start()
            else:
                print(len(self.messages))
            time.sleep(.1)

    def on_move(self, x, y):
        self.messages.append('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(self, x, y, button, pressed):
        self.messages.append('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))

    def on_scroll(self, x, y, dx, dy):
        self.messages.append('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
