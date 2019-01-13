import unittest
import sys

sys.modules["picamera"] = __import__("ambieye.test.mock.picamera", fromlist=['object'])
import ambieye.__main__ as ambieye

class TestStringMethods(unittest.TestCase):

    def test_main(self):
        ambieye.main([])


if __name__ == '__main__':
    unittest.main()
