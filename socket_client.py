# ## From https://stackoverflow.com/questions/30988033/sending-live-video-frame-over-network-in-python-opencv
import threading
import time

from numpysocket import NumpySocket
import cv2

host_ip = 'localhost'  # change me

npSocket = NumpySocket()
npSocket.startClient(host_ip, 8001)
frames = {
    "len": 0
}

frames_ = []
frames_processed = []


class PlayerThread(threading.Thread):
    running = True
    current_t = 0

    def __init__(self):
        super(PlayerThread, self).__init__()

    def run(self) -> None:
        while self.running:

            if len(frames_) > 10:
                for i in range(0, len(frames_)):
                    try:
                        cv2.imshow("frame", frames_[i])
                        frames_.pop(0)
                    except IndexError:
                        pass

                    if cv2.waitKey(60) & 0xFF == ord('q'):
                        break
            time.sleep(.1)
            self.current_t += 1
PlayerThread_ = PlayerThread()
player_started = False
# Read until video is completed
while True:
    # Capture frame-by-frame
    frame = npSocket.recieve()
    cv2.imshow('Frame', frame)
    # Press Q on keyboard to  exit
    if cv2.waitKey(60) & 0xFF == ord('q'):
       break
    cv2.waitKey(delay=int(1000 / 60));
print("Closing")
npSocket.close()
