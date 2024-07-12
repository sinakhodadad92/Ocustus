from error_detection.utilities import MM_TO_PIXEL, mm_to_pixel, img_to_pil_image


def get_board_coordinates(img, config):
    # Size of the image in pixels (size of original image)
    width, height = img.size

    MM_TO_PIXEL["X"] = width / config["panel"]["width"]
    MM_TO_PIXEL["Y"] = height / config["panel"]["height"]

    # Change origin
    config["panel"]["panelOffsetOriginX"] = config["panel"]["panelOffsetOriginX"]

    final_config = {
        "board_width": mm_to_pixel(config["board"]["width"], "X"),
        "board_height": mm_to_pixel(config["board"]["height"], "Y"),
        "border_margin_X": mm_to_pixel(config["panel"]["panelOffsetOriginX"], "X"),
        "border_margin_Y": mm_to_pixel(config["panel"]["panelOffsetOriginY"], "Y"),
        "board_buffer_X": mm_to_pixel(config["panel"]["boardOffsetX"], "X") - mm_to_pixel(config["board"]["width"], "X"),
        "board_buffer_Y": mm_to_pixel(config["panel"]["boardOffsetY"], "Y") - mm_to_pixel(config["board"]["height"], "Y"),
        "number_of_columns": config["panel"]["numberOfColumns"],
        "number_of_rows": config["panel"]["numberOfRows"]
    }

    assembledBoards = config['panel']['assembledBoards']

    # Iterating rows in reverse order
    # AISLER convention i.e. board counting starts from the bottomost row and leftmost column
    coordinatesList = []
    boards_count = 0
    for r in reversed(range(final_config["number_of_rows"])):
        for c in range(final_config["number_of_columns"]):
            x1 = final_config["border_margin_X"] + c*(
                final_config["board_width"] + final_config["board_buffer_X"])
            y1 = final_config["border_margin_Y"] + r*(
                final_config["board_height"] + final_config["board_buffer_Y"])
            x2 = final_config["border_margin_X"] + c*(
                final_config["board_width"] + final_config["board_buffer_X"]) + final_config["board_width"]
            y2 = final_config["border_margin_Y"] + r*(
                final_config["board_height"] + final_config["board_buffer_Y"]) + final_config["board_height"]
            coordinatesList.append((x1, y1, x2, y2))
            boards_count += 1
            if assembledBoards and boards_count >= assembledBoards:  # Process only assembled boards
                return coordinatesList

    return coordinatesList


def board_detection(panel, panel_config):

    panel['img'] = img_to_pil_image(panel['img'])
    coordinates_list = get_board_coordinates(panel['img'], panel_config)

    boards = []
    for index, coordinates in enumerate(coordinates_list):
        image = panel['img'].crop(coordinates)
        boards.append({
            'id': index+1,
            'panel_id': panel['id'],
            'img': image,
            'coordinates': coordinates
        })

    return boards


def board_detection_multi(panels, panel_config):
    print("Identify, crop and save boards from panels\n")
    boards = []
    for panel in panels:
        boards = boards + board_detection(panel, panel_config)
    return boards
