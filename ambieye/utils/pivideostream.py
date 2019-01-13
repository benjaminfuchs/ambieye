from threading import Thread
import logging
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import colorutils

LOGGER = logging.getLogger("root")

class PiVideoStream:

    def __init__(self, resolution=(640, 480), framerate=5, gamma=0):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
        self.image = None
        self.stopped = False
        self.gamma = gamma

    def start(self):
        LOGGER.info("starting video stream...")
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self

    def update(self):
        for frame in self.stream:
            self.image = frame.array
            self.rawCapture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

            time.sleep(0.033)

    def read(self):
        if self.gamma != 0:
            return colorutils.adjust_gamma(self.image, self.gamma)
        return self.image

    def stop(self):
        self.stopped = True
