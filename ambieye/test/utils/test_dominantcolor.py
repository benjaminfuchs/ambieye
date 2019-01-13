import os
import unittest
import ambieye.utils.dominantcolor as dominantcolor

TEST_IMAGE = os.path.join(os.path.dirname(__file__), "image", "icon.jpg")

class TestStringMethods(unittest.TestCase):

    def test_get_dominant_color(self):
        result = dominantcolor.get_dominant_color(TEST_IMAGE)
        expected = [199, 57, 180]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
