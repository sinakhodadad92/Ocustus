from error_detection.background_removal import background_removal_multi
from error_detection.board_detection import board_detection_multi
from error_detection.components_detection import components_detection
from error_detection.image_diff import error_detection
from error_detection.format_data import finalize_result
from error_detection.utilities import read_json, read_csv
import cv2


def run(panel_tuples, panel_config, components_config):
    print("Pipeline started")

    print("Step1: ")
    cropped_panels = background_removal_multi(panel_tuples)

    print("Step2: ")
    boards = board_detection_multi(cropped_panels, panel_config)

    print("Step3: ")
    component_dict = components_detection(
        boards, panel_config["board"], components_config)

    print("Step4: ")
    component_errors = error_detection(component_dict)

    print("Step5: ")
    result = finalize_result(
        cropped_panels, component_errors, components_config)

    print("Pipeline finished successfully")
    return result


def run_with_paths(panel_tuples, panel_config_path, components_config_path):
    # Read panel images, panel config and components config
    panels = []
    for panel_tuple in panel_tuples:
        panels.append((panel_tuple[0], cv2.imread(panel_tuple[1])))
    panel_config = read_json(panel_config_path)
    components_config = read_csv(components_config_path)

    return run(panels, panel_config, components_config)
