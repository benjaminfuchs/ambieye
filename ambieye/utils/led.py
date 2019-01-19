from threading import Thread
import logging
import requests
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import colorutils

LOGGER = logging.getLogger("root")

class LedThread:

    def __init__(self):
        self.target_color = [0, 0, 0]
        self.current_color = [0, 0, 0]
        self.stopped = False

    def start(self):
        LOGGER.info("starting light thread...")
        t = Thread(target=self.update)
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.target_color != self.current_color:
                LOGGER.debug("update() %s", self.current_color)
                self.current_color = colorutils.limit_diff(self.current_color, self.target_color, 3)
                LedThread.send_color(self.current_color)

            if self.stopped:
                return

            time.sleep(0.033)

    def set_color(self, color):
        LOGGER.debug("set_color() %s", color)
        self.target_color = color

    def stop(self):
        self.stopped = True

    @staticmethod
    def send_color(color):
        color = [min(255, max(10, color[0] * 1.1)), min(255, max(10, color[1] * 1.1)), min(255, max(10, color[2] * 1.1))]
        hex_color = colorutils.to_hex_color_string(color)
        LOGGER.debug("hex_color: %s", hex_color)
        try:
            r = requests.post("http://192.168.178.23:5000/save_settings", json={"led.brightness": 1, "led.color": hex_color})
        except requests.exceptions.ConnectionError as exception:
            LOGGER.error("Could not send color! (%s)", str(exception))
        LOGGER.debug("status: %s", r.status_code)
