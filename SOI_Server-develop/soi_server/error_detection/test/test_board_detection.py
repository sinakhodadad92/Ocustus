import unittest

from PIL import Image

from error_detection.board_detection import board_detection
from error_detection.utilities import read_json


class MyTestCase(unittest.TestCase):
    def test_board_detection(self):
        """Checks if board detection returns 4 images from the panel test image"""
        panel_config_path = "data/panel_config.json"
        panel_config = read_json(panel_config_path)
        panel = {
            'id': 0,
            'img': Image.open("error_detection/test/component_detection_test.jpg")
        }
        boards = board_detection(panel, panel_config)
        self.assertEqual(len(boards), 3)


if __name__ == '__main__':
    unittest.main()
