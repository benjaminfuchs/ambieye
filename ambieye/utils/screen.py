import logging
import cv2
import colorutils

LOGGER = logging.getLogger("root")

class Screen:

    def __init__(self, resolution=(640, 480)):
        self.avg = None
        self.diff = 50
        self.resolution = resolution
        self.x = resolution[0]/4
        self.y = resolution[1]/4
        self.w = self.x * 3
        self.h = self.y * 3
        self.set = False
        self.screen_x = 0
        self.screen_y = 0
        self.screen_w = 0
        self.screen_h = 0

    def set_border(self, x, y, w, h):
        self.set = True
        self.screen_x = x
        self.screen_y = y
        self.screen_w = w
        self.screen_h = h

    def get_screen_cordinates(self, image):
        new_x = self.x
        new_y = self.y
        new_w = self.w
        new_h = self.h

        # resize the frame, convert it to grayscale, and blur it
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the average frame is None, initialize it
        if self.avg is None:
            LOGGER.debug("starting background model...")
            self.avg = gray.copy().astype("float")

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        cv2.accumulateWeighted(gray, self.avg, 0.5)

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 5, 255,
            cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        if cnts:
            c = max(cnts, key = cv2.contourArea)
            if cv2.contourArea(c) > 5000:
                LOGGER.debug("found contour")
                new_x, new_y, new_w, new_h = cv2.boundingRect(c)
                self.diff = max(self.diff - 1, 1)

        array = colorutils.limit_diff([self.x, self.y, self.w, self.h], [new_x, new_y, new_w, new_h], self.diff)

        if (array[0] < self.screen_x + 10 and array[0] > self.screen_x - 10) or not self.set:
            self.x = array[0]
        if (array[1] < self.screen_y + 10 and array[1] > self.screen_y - 10) or not self.set:
            self.y = array[1]
        if (array[2] < self.screen_w + 10 and array[2] > self.screen_w - 10) or not self.set:
            self.w = array[2]
        if (array[3] < self.screen_h + 10 and array[3] > self.screen_h - 10) or not self.set:
            self.h = array[3]

        LOGGER.debug("x: %s, y: %s, w: %s, h: %s", str(self.x), str(self.y), str(self.w), str(self.h))
        return self.x, self.y, self.w, self.h
