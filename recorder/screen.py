import ctypes
import threading
from io import BytesIO
import cv2
import pyautogui
import numpy as np
from recorder.process_video import save_video
import logging


class RecorderScreen(threading.Thread):
    SCREEN_SIZE = None
    fourcc = None
    fps = None
    out = None
    record_seconds = 0
    current_t = 0
    recording = True
    monitors = {
        "1": None,
        "2": None
    }
    main_controller = None
    frames = None
    current_monitor = 1

    def get_monitor(self, monitor_id):
        if monitor_id == 1:
            return int(0), int(0), int(self.screensize[0] - self.Primary_SCREEN_SIZE[0]), int(self.screensize[1])
        elif monitor_id == 2:
            return int(self.screensize[0] - self.Primary_SCREEN_SIZE[0]), int(0), int(self.screensize[0] - self.Primary_SCREEN_SIZE[0]), int(self.screensize[1])
        return None

    def __init__(self, main_controller_instance, record_seconds=None, fps=None, output_filename=None, monitor_id=None):
        self.main_controller = main_controller_instance
        self.frames = []
        self.screensize = ctypes.windll.user32.GetSystemMetrics(78), ctypes.windll.user32.GetSystemMetrics(79)
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
        self.out = cv2.VideoWriter(self.output_filename, 0x7634706d, self.fps, self.SCREEN_SIZE)
        self.record_seconds = record_seconds if record_seconds is not None else 10
        if monitor_id is not None:
            self.current_monitor = self.get_monitor(monitor_id)
        print(self.current_monitor)
        super(RecorderScreen, self).__init__()

    @staticmethod
    def __pack_frame(frame):
        f = BytesIO()
        np.savez(f, frame=frame)

        packet_size = len(f.getvalue())
        header = '{0}:'.format(packet_size)
        header = bytes(header.encode())  # prepend length of array

        out = bytearray()
        out += header

        f.seek(0)
        out += f.read()
        return out

    def send(self, frame, socket):
        if not isinstance(frame, np.ndarray):
            raise TypeError("input frame is not a valid numpy array")

        out = self.__pack_frame(frame)
        try:
            socket.sendall(out)
        except ConnectionResetError as e:
            self.main_controller.print_data("reset", prefix="err:")
            return False
        logging.info("frame sent")

    def run(self) -> None:
        self.current_t = 0
        if self.record_seconds == -1:
            while self.recording:
                self.current_t += 1
                img = pyautogui.screenshot(region=self.current_monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resize = frame[::2, ::2]
                self.frames.append(frame)
                current_clients = self.main_controller.SocketServer_.server_process.server.clients
                try:
                    if len(current_clients.keys()) > 0:
                        for c_uuid in self.main_controller.SocketServer_.server_process.server.clients.keys():
                            try:
                                c_ = self.main_controller.SocketServer_.server_process.server.clients[c_uuid]
                                try:
                                    self.send(frame_resize, c_["client"])

                                except ConnectionResetError as e:
                                    self.main_controller.print_data("client closed", prefix="net")
                                    del self.main_controller.SocketServer_.server_process.server.clients[c_uuid]
                                except ConnectionAbortedError as e:
                                    self.main_controller.print_data("client aborted", prefix="net")
                                    del self.main_controller.SocketServer_.server_process.server.clients[c_uuid]
                                    print(len(self.main_controller.SocketServer_.server_process.server.clients))
                            except KeyError:
                                pass
                except RuntimeError:
                    current_clients = self.main_controller.SocketServer_.server_process.server.clients
                    pass
                # self.main_controller.print_data("current frame: "+str(len(self.frames)), prefix="rec")
                self.out.write(frame)

                if cv2.waitKey(1) == ord("q"):
                    break

            self.main_controller.print_data("stoppped recording after: "+str(self.current_t), prefix="rec:")

        elif isinstance(self.record_seconds, int) and self.record_seconds != "-1":
            self.current_t = 0
            for i in range(int(self.record_seconds * self.fps)):
                if not self.recording:
                    break
                self.current_t = i
                img = pyautogui.screenshot(region=self.current_monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frames.append(frame)
                # self.main_controller.print_data("current frame: " + str(len(self.frames)), prefix="rec")

                self.out.write(frame)
                if cv2.waitKey(1) == ord("q"):
                    break

            filename_fileparts = [
                self.output_filename.split(".")[0] + "-processed",
                self.output_filename.split(".")[1]
            ]

            processed_filename = ".".join(filename_fileparts)
            if self.current_monitor is not None:
                monitor_width = self.current_monitor[2]
                monitor_height = self.current_monitor[3]
            self.main_controller.print_data("stoppped recording after: " + str(self.current_t)+" frames", prefix="rec:")

        cv2.destroyAllWindows()
        self.out.release()
        save_video(
            self.output_filename,
            processed_filename,
            monitor_width,
            monitor_height,
            self.fps
        )
