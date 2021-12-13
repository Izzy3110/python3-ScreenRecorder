import threading
import time


class ObserveRecording(threading.Thread):
    current_recording_status = False
    main_while_instance = None
    main_controller_instance = None

    def __init__(self, mainwhile_instance, main_controller_instance):
        self.main_controller_instance = main_controller_instance
        self.main_while_instance = mainwhile_instance
        self.RecorderScreenInstance = self.main_controller_instance.RecorderScreen_
        super(ObserveRecording, self).__init__()

    def run(self) -> None:
        while self.main_while_instance.main_loop_running:
            if self.current_recording_status != self.RecorderScreenInstance.recording:
                self.current_recording_status = self.RecorderScreenInstance.recording
            if not self.RecorderScreenInstance.is_alive():
                if self.main_controller_instance.server_started:
                    self.main_controller_instance.stop_socket_server()
                    self.main_while_instance.stop()
                    self.main_while_instance.main_loop_running = False
            time.sleep(.1)
