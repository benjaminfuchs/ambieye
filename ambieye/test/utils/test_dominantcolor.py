import os
import unittest
import cv2
import ambieye.utils.dominantcolor as dominantcolor

TEST_IMAGE = os.path.join(os.path.dirname(__file__), "image", "icon.jpg")

class TestStringMethods(unittest.TestCase):

    def test_get_dominant_color(self):
        # read in image of interest
        bgr_image = cv2.imread(TEST_IMAGE)
        # convert to HSV; this is a better representation of how we see color
        hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        # extract dominant color 
        result = dominantcolor.get_dominant_color(hsv_image)
        expected = [199, 57, 180]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
