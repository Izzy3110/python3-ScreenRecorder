from recorder.screen import RecorderScreen
from server.sserver import SocketServer


class MainController:
    SocketServer_ = None
    RecorderScreen_ = None
    started_ = False

    def get_started(self):
        return self.started_

    def start_server(self):
        self.SocketServer_ = SocketServer()
        self.SocketServer_.start()

    def stop_server(self):
        self.SocketServer_.server_process.server.stop()
        self.SocketServer_.server_process.stop()
        self.SocketServer_.running = False

    def start_record(self, recording_seconds):
        self.RecorderScreen_ = RecorderScreen(record_seconds=recording_seconds if recording_seconds is not None else -1)
        self.RecorderScreen_.start()

    def stop_record(self):
        self.RecorderScreen_.recording = False
