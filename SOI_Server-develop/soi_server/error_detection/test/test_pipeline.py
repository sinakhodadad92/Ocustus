import unittest
import cv2
from error_detection.pipeline import *
from error_detection.utilities import read_json, read_csv


def was_error_detected(components, designator, panel_id, board_id):
    print("Check component", designator, "on panel", panel_id, "on board", board_id)
    for component in components:
        if component['designator'] == designator:
            component_errors = component['errors']
    if component_errors is None:
        return False
    for component_error in component_errors:
        if board_id == component_error['board_id'] and panel_id == component_error['panel_id']:
            return True
    return False

def test_pipeline(image_paths, panel_config_path, component_config_path):
    tuples = []
    for i in range(len(image_paths)):
        tuples.append((i+1,image_paths[i]))
    errors_dict_list = run_with_paths(tuples, panel_config_path, component_config_path)


class PipelineTest(unittest.TestCase):

    def test_run_with_paths(self):
        errors = [("C3", 1, 1), ("R3", 1, 1), ("R4", 1, 1), ("R6", 1, 1), ("R8", 1, 1)]
        panel_tuples = [(1, "error_detection/test/test_panel_images/raw_input_rotated.jpg")]
        panel_config_path = "data/panel_config.json"
        components_config_path = "data/components_config.csv"

        components = run_with_paths(panel_tuples, panel_config_path, components_config_path)['components']
        for (error_designator, panel_id, board_id) in errors:
            self.assertTrue(was_error_detected(components, error_designator, panel_id, board_id))

    def test_run_2_panels(self):
        errors = [("C3", 1, 1), ("R3", 1, 1), ("R6", 1, 1), ("R4", 1, 1), ("R8", 1, 1),
                  ("C3", 2, 1), ("R3", 2, 1), ("R6", 2, 1), ("R4", 2, 1), ("R8", 2, 1)]
        panel_tuples = [(1, "error_detection/test/test_panel_images/raw_input_rotated.jpg"), (2,"error_detection/test/test_panel_images/cropped_panel.jpg")]

        panel_config_path = "data/panel_config.json"
        components_config_path = "data/components_config.csv"

        components = run_with_paths(panel_tuples, panel_config_path, components_config_path)['components']
        for (error_designator, panel_id, board_id) in errors:
            self.assertTrue(was_error_detected(components, error_designator, panel_id, board_id))


if __name__ == '__main__':
    unittest.main()
