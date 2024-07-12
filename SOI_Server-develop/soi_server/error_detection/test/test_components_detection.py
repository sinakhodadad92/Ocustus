import unittest

from board_detection import get_board_coordinates
from components_detection import *
from utilities import *
from PIL import Image


class MyTestCase(unittest.TestCase):

    def test_components_detection(self):
        """Tests if components_detection returns a dict with each designator as key and the same number of
        component images for each designator as there are boards"""

        panel_config_path = "data/panel_config.json"
        components_config_path = "data/components_config.csv"
        boards_path = "error_detection/test/test_board_images/"
        board_names = ["board_1", "board_2", "board_3"]
        boards = []
        panel_config = read_json(panel_config_path)
        components_config = read_csv(components_config_path)
        panel_img = Image.open("error_detection/test/test_panel_images/cropped_panel.jpg")
        coordinates_list = get_board_coordinates(panel_img, panel_config)

        for i in range(len(board_names)):
            boards.append({
                'id': i+1,
                'panel_id': 1,
                'img': Image.open(boards_path+board_names[i]+".jpg"),
                'coordinates': coordinates_list[i]
            })

        components_dict = components_detection(boards, panel_config["board"], components_config)

        for component in components_config:
            designator = component["DESIGNATOR"]
            if component["ID"] != 'N/A': # exclude holes
                self.assertIn(designator, components_dict)
                self.assertEqual(len(components_dict[designator]), len(boards))


if __name__ == '__main__':
    unittest.main()
