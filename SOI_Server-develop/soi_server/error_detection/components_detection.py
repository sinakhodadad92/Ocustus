from error_detection.utilities import MM_TO_PIXEL, mm_to_pixel, img_to_pil_image

DEFAULT_SQUARE_SIDE_LENGTH_HALF = 3


def get_component_rectangle_coordinates(component):
    if component['SIZE_MM']:
        SQUARE_SIDE_LENGTH_HALF = float(component['SIZE_MM'])
    else:
        SQUARE_SIDE_LENGTH_HALF = DEFAULT_SQUARE_SIDE_LENGTH_HALF

    return (mm_to_pixel(component['X-POSITION']-SQUARE_SIDE_LENGTH_HALF, "X"), mm_to_pixel(component['Y-POSITION']-SQUARE_SIDE_LENGTH_HALF, "Y"),
            mm_to_pixel(component['X-POSITION']+SQUARE_SIDE_LENGTH_HALF, "X"), mm_to_pixel(component['Y-POSITION']+SQUARE_SIDE_LENGTH_HALF, "Y"))


def is_valid_component(component):
    return (component["COMPONENT VALUE"] != 'N/A' and component["ID"] != 'N/A')


# Returns component origin(x,y) in panel coordinate system
def get_component_coordinate(component, board_coordinates):
    return (mm_to_pixel(component['X-POSITION'], "X") + board_coordinates[0], mm_to_pixel(component['Y-POSITION'], "Y") + board_coordinates[1])


def identify_board_components(board, board_config, components_config):
    board['img'] = img_to_pil_image(board['img'])
    width, height = board['img'].size
    MM_TO_PIXEL["X"] = width / board_config["width"]
    MM_TO_PIXEL["Y"] = height / board_config["height"]
    components_list = []

    for component in components_config:
        component_rectangle_coordinates = get_component_rectangle_coordinates(
            component)
        image = board['img'].crop(component_rectangle_coordinates)
        component_coordinate = get_component_coordinate(
            component, board['coordinates'])
        components_list.append({
            'designator': component["DESIGNATOR"],
            'img': image,
            'coordinates': component_coordinate,
            'board_id': board['id'],
            'panel_id': board['panel_id']
        })

    return components_list


def add_components_to_dict(component_dict, component_list):
    for component in component_list:
        if component['designator'] not in component_dict:
            component_dict[component['designator']] = []
        component_dict[component['designator']].append({
            'img': component['img'],
            'coordinates': component['coordinates'],
            'board_id': component['board_id'],
            'panel_id': component['panel_id']
        })
    return component_dict


def preprocess_components(components_config, board_config):
    components = []
    for component in components_config:
        if is_valid_component(component):  # Remove invalid component
            # Change origin
            component['X-POSITION'] = float(component['X-POSITION'])
            component['Y-POSITION'] = board_config['height'] - \
                float(component['Y-POSITION'])

            components.append(component)
    return components


def components_detection(boards, board_config, components_config):
    print("Detect and crop board components\n")

    components = preprocess_components(components_config, board_config)

    component_dict = {}
    for board in boards:
        component_list = identify_board_components(
            board, board_config, components)
        component_dict = add_components_to_dict(component_dict, component_list)
    return component_dict
