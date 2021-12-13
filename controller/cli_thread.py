import sys
import threading
import time


class CLIThread(threading.Thread):
    main_loop_running = True
    MainController = None

    def __init__(self, main_controller_instance):
        self.MainController = main_controller_instance
        super(CLIThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self) -> None:
        first_sleep = True
        start_sleep_time = 2

        while self.main_loop_running:
            if first_sleep:
                time.sleep(start_sleep_time)
                first_sleep = False
            user_input = input("> ")
            if user_input == "start":
                if not self.MainController.server_started:
                    self.MainController.start_socket_server()
                    self.MainController.server_started = True
                else:
                    print("already started")
                time.sleep(2)

            elif user_input == "stop":
                if self.MainController.server_started:
                    self.MainController.stop_socket_server()
                    self.MainController.server_started = False
                else:
                    print("already stopped")
                time.sleep(2)

            elif user_input == "screen cross":
                print("crossing")
                time.sleep(2)

            elif user_input == "record":
                self.MainController.start_record(
                    recording_seconds=self.MainController.recording_seconds,
                    fps=self.MainController.DEFAULT_RECORD_FPS)
                time.sleep(2)

            elif user_input == "stoprec":
                self.MainController.stop_record()
                time.sleep(2)
            elif user_input == "exit":
                if self.MainController.server_started:
                    if self.MainController.RecorderScreen_.recording:
                        self.MainController.stop_record()
                    self.MainController.stop_socket_server()
                    self.main_loop_running = False
                    self.stop()
                    self.MainController.server_started = False
                    break
                print("exited by user")
                sys.exit(0)

