import ctypes
import threading
import cv2
import pyautogui
import numpy as np

user32 = ctypes.windll.user32


class RecorderScreen(threading.Thread):
    SCREEN_SIZE = None
    fourcc = None
    fps = None
    out = None
    record_seconds = 0
    first_monitor = None
    second_monitor = None
    current_t = 0
    recording = True

    def get_monitor(self, monitor_id):
        if monitor_id == 1:
            return 0, 0, self.screensize[0] - self.Primary_SCREEN_SIZE[0], self.screensize[1]
        elif monitor_id == 2:
            return self.screensize[0] - self.Primary_SCREEN_SIZE[0], 0, self.screensize[0] - self.Primary_SCREEN_SIZE[0], self.screensize[1]

    def __init__(self, record_seconds=None, fps=None, output_filename=None):

        self.screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
        self.Primary_SCREEN_SIZE = tuple(pyautogui.size())

        # display screen resolution, get it using pyautogui itself
        self.SCREEN_SIZE = tuple(pyautogui.size())
        # define the codec
        self.fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        # frames per second

        self.fps = 10.0
        if fps is not None:
            self.fps = int(fps)

        self.output_filename = output_filename if output_filename is not None else "output.mp4"

        # create the video write object
        self.out = cv2.VideoWriter(self.output_filename, 0x7634706d, self.fps, self.SCREEN_SIZE)
        # the time you want to record in seconds
        self.record_seconds = record_seconds if record_seconds is not None else 10
        self.first_monitor = self.get_monitor(1)

        super(RecorderScreen, self).__init__()

    def run(self) -> None:
        self.current_t = 0
        if self.record_seconds == -1:
            while self.recording:
                self.current_t += 1
                # print("frame:" + str(self.current_t))
                # make a screenshot
                img = pyautogui.screenshot(region=self.first_monitor)
                # convert these pixels to a proper numpy array to work with OpenCV
                frame = np.array(img)
                # convert colors from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # write the frame
                self.out.write(frame)
                # show the frame
                # cv2.imshow("screenshot", frame)
                # if the user clicks q, it exits
                if cv2.waitKey(1) == ord("q"):
                    break
            print("stoppped recording after: "+str(self.current_t))
        elif isinstance(self.record_seconds, int) and self.record_seconds != "-1":
            self.current_t = 0
            for i in range(int(self.record_seconds * self.fps)):
                if not self.recording:
                    break
                self.current_t = i
                # print("frame:"+str(self.current_second))
                # make a screenshot
                img = pyautogui.screenshot(region=self.first_monitor)
                # convert these pixels to a proper numpy array to work with OpenCV
                frame = np.array(img)
                # convert colors from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # write the frame
                self.out.write(frame)
                # show the frame
                # cv2.imshow("screenshot", frame)
                # if the user clicks q, it exits
                if cv2.waitKey(1) == ord("q"):
                    break
            print("stoppped recording after: " + str(self.current_t)+" frames")

        # make sure everything is closed when exited
        cv2.destroyAllWindows()
        self.out.release()
