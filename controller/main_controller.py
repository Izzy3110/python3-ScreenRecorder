import os

from recorder.screen import RecorderScreen
from server.socket_server import SocketServer


class MainController:
    DEFAULT_RECORD_FPS = 60
    DEFAULT_OPTIONS = {
        "autostart": True,
        "recording_seconds": 10,
        "record_at_start": True,
        "stop_after_record": True
    }
    recording_seconds = None
    SocketServer_ = None
    RecorderScreen_ = None
    started_ = False
    server_started = None
    stop_after_record = False
    project_path = None
    current_monitor = 1

    def __init__(self , project_path):
        self.project_path = project_path
        self.server_started = False

    def print_data(self, message, prefix=None):
        print(" ".join([prefix if prefix is not None else "txt:", message]))

    def get_started(self):
        return self.started_

    def start_socket_server(self):
        self.SocketServer_ = SocketServer(self)
        self.SocketServer_.start()

    def stop_socket_server(self):
        self.SocketServer_.server_process.server.stop()
        self.SocketServer_.server_process.stop()
        self.SocketServer_.running = False

    def start_record(self, recording_seconds, fps=None, monitor_id=None):
        if monitor_id is not None:
            print("using monitor: "+str(monitor_id))
            self.current_monitor = monitor_id

        self.print_data("recording for "+str(recording_seconds)+" seconds at "+str(fps)+" fps", prefix="rec:")
        self.RecorderScreen_ = RecorderScreen(
            self,
            record_seconds=recording_seconds if recording_seconds is not None else -1,
            fps=fps,
            output_filename=os.path.join(self.project_path, "data", "output.mp4") if self.project_path is not None else "output.mp4",
            monitor_id=self.current_monitor
        )
        self.RecorderScreen_.start()

    def stop_record(self):
        self.RecorderScreen_.recording = False
