import sys
import time
import threading
import ctypes

from recorder.screen import RecorderScreen
from server.sserver import SocketServer

user32 = ctypes.windll.user32


class ObserveRecording(threading.Thread):
    current_recording_status = False

    def __init__(self, recorder_screen_i):
        self.RecorderScreenInstance = recorder_screen_i
        super(ObserveRecording, self).__init__()

    def run(self) -> None:
        while MainWhile_.main_loop_running:
            if self.current_recording_status != self.RecorderScreenInstance.recording:
                self.current_recording_status = self.RecorderScreenInstance.recording
            if not self.RecorderScreenInstance.is_alive():
                if started_:
                    MainController_.stop_server()
                    MainWhile_.stop()
                    MainWhile_.main_loop_running = False
            time.sleep(.1)


class MainController:
    SocketServer_ = None
    RecorderScreen_ = None

    def start_server(self):
        self.SocketServer_ = SocketServer()
        self.SocketServer_.start()

    def stop_server(self):
        self.SocketServer_.server_process.server.stop()
        self.SocketServer_.server_process.stop()
        self.SocketServer_.running = False

    def start_record(self):
        self.RecorderScreen_ = RecorderScreen(record_seconds=recording_seconds if recording_seconds is not None else -1)
        self.RecorderScreen_.start()

    def stop_record(self):
        self.RecorderScreen_.recording = False


class MainWhile(threading.Thread):
    main_loop_running = True

    def __init__(self):
        super(MainWhile, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        global started_
        first_sleep = True
        start_sleep_time = 2

        while self.main_loop_running:
            if first_sleep:
                time.sleep(start_sleep_time)
                first = False
            user_input = input("> ")
            if user_input == "start":
                if not started_:
                    MainController_.start_server()
                    started_ = True
                else:
                    print("already started")
                time.sleep(2)

            elif user_input == "stop":
                if started_:
                    MainController_.stop_server()
                    started_ = False
                else:
                    print("already stopped")
                time.sleep(2)

            elif user_input == "screen cross":
                print("crossing")
                time.sleep(2)

            elif user_input == "record":
                MainController_.start_record()
                time.sleep(2)

            elif user_input == "stoprec":
                MainController_.stop_record()
                time.sleep(2)
            elif user_input == "exit":
                if started_:
                    if MainController_.RecorderScreen_.recording:
                        MainController_.stop_record()
                    MainController_.stop_server()
                    self.main_loop_running = False
                    self.stop()
                    break

                print("exited by user")
                sys.exit(0)


if __name__ == '__main__':
    recording_seconds = None
    options_ = {
        "autostart": True,
        "recording_seconds": 10,
        "record_at_start": True,
        "stop_after_record": True
    }
    stop_after_record = False
    started_ = False

    MainController_ = MainController()
    MainWhile_ = MainWhile()

    if len(sys.argv) > 1:
        valid_keys = ["seconds"]
        for i in range(1, len(sys.argv)):
            current_item = sys.argv[i]
            key, val = current_item.split("=")
            if key in valid_keys:
                if key == "seconds":
                    recording_seconds = val if isinstance(val, int) else int(val)
                    if "record_at_start" in options_.keys():
                        if not options_["record_at_start"]:
                            options_["record_at_start"] = True

    if "recording_seconds" not in options_.keys():
        recording_seconds = int(options_["recording_seconds"]) \
            if not isinstance(options_["recording_seconds"], int) else options_["recording_seconds"]

    if options_["autostart"] and not started_:
        MainController_.start_server()
        started_ = True

    if "record_at_start" in options_.keys():
        # print("recording starting at start for: "+str(recording_seconds))
        MainController_.start_record()
        ObserveRecording_ = ObserveRecording(MainController_.RecorderScreen_)
        ObserveRecording_.start()
        MainWhile_.start_sleep_time = 4

    if "stop_after_record" in options_.keys() and options_["stop_after_record"]:
        # print("stopping after record")
        stop_after_record = True
