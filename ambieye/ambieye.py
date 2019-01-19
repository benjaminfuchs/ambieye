#!/usr/bin/python
import argparse
import sys
import time
import logging
import picamera
import cv2
import utils.args as args
import utils.colorutils as colorutils
import utils.log as log
from utils.led import LedThread
from utils.pivideostream import PiVideoStream
from utils.screen import Screen
import sys, signal

LOGGER = logging.getLogger("root")
THREADS = []

def get_args(arguments):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-k", "--num-means", default=4, type=int)
    parser.add_argument("-i", "--processing-size", default=25, type=int)
    parser.add_argument("-g", "--gamma", default=1, type=float)
    parser.add_argument("-b", "--brightness", default=0, type=int)
    args.add_log_level(parser)
    return parser.parse_args(arguments)

def signal_handler(_, __):
    for thread in THREADS:
        thread.stop()
    sys.exit(0)

def debug_image():
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.resolution = (640, 480)
        camera.capture("debug_snapshot.jpg")

def blink():
    LedThread.send_color((0, 0, 0))
    time.sleep(0.5)
    LedThread.send_color((255, 255, 255))
    time.sleep(0.5)
    LedThread.send_color((0, 0, 0))

def loop(brightness, num_means, processing_size, gamma, debug):
    old_x, old_y, old_w, old_h = 0, 0, 0, 0
    count = 0

    thread_stream = PiVideoStream(gamma=gamma)
    THREADS.append(thread_stream)
    thread_stream.start()
    time.sleep(1)
    screen = Screen()

    blink()
    LOGGER.info("searching screen...")

    while True:
        image = thread_stream.read()
        x, y, w, h = screen.get_screen_cordinates(image)

        if x < old_x + 10 and x > old_x - 10 and y < old_y + 10 and y > old_y - 10 \
            and w < old_w + 10 and w > old_w - 10 and h < old_h + 10 and h > old_h - 10:
            count = count + 1
        else:
            count = 0
        old_x, old_y, old_w, old_h = x, y, w, h
    
        if count > 50:
            break

    blink()
    screen.set_border(x, y, w, h)
    LOGGER.info("found screen")

    led_thread = LedThread()
    THREADS.append(led_thread)
    led_thread.start()

    while True:
        signal.signal(signal.SIGINT, signal_handler)
        image = thread_stream.read()
        x, y, w, h = screen.get_screen_cordinates(image)
        crop_img = image[y:y+h, x:x+w]
        if debug:
            cv2.imwrite("debug_screen.jpg" , crop_img)
        try:
            color = colorutils.get_dominant_color(crop_img, \
                brightness, num_means, processing_size)
        except Exception as exception:
            LOGGER.error("Could not get dominant color! (%s)", str(exception))
        led_thread.set_color(color)

        time.sleep(0.033)

    for thread in THREADS:
        thread.stop()

def main(argv):
    arguments = get_args(argv)
    log.setup_custom_logger(LOGGER, arguments.log_level)
    debug = False

    if arguments.log_level == "DEBUG":
        debug = True

    if debug:
        debug_image()

    loop(arguments.brightness, arguments.num_means, arguments.processing_size, arguments.gamma, debug)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
