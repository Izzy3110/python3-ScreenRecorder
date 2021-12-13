import sys
from recorder.observer import ObserveRecording


def parse_commandline_options(main_controller_instance, main_while_instance):
    options_ = main_controller_instance.DEFAULT_OPTIONS
    if len(sys.argv) > 1:
        valid_keys = ["seconds", "fps"]
        for i in range(1, len(sys.argv)):
            current_item = sys.argv[i]
            key, val = current_item.split("=")
            if key in valid_keys:
                if key == "seconds":
                    main_controller_instance.recording_seconds = val if isinstance(val, int) else int(val)
                    if "record_at_start" in options_.keys():
                        if not options_["record_at_start"]:
                            options_["record_at_start"] = True
                elif key == "fps":
                    fps = val if isinstance(val, int) else int(val)
                    if "record_fps" not in options_.keys():
                        options_["record_fps"] = fps

    if "recording_seconds" not in options_.keys():
        main_controller_instance.recording_seconds = int(options_["recording_seconds"]) \
            if not isinstance(options_["recording_seconds"], int) else options_["recording_seconds"]

    if options_["autostart"] and not main_controller_instance.server_started:
        main_controller_instance.start_socket_server()
        main_controller_instance.server_started = True

    if "record_at_start" in options_.keys():
        main_controller_instance.start_record(
            recording_seconds=main_controller_instance.recording_seconds,
            fps=options_["record_fps"] if "record_fps" in options_.keys() else main_controller_instance.DEFAULT_RECORD_FPS
        )
        ObserveRecording_ = ObserveRecording(main_while_instance, main_controller_instance)
        ObserveRecording_.start()
        main_while_instance.start_sleep_time = 4

    if "stop_after_record" in options_.keys() and options_["stop_after_record"]:
        main_controller_instance.stop_after_record = True
