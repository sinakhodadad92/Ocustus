import csv
import json
from PIL import Image
import numpy


def read_csv(csv_path):
    components = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            components.append(row)
    return components


def read_json(path):
    data = None
    with open(path) as f:
        data = json.load(f)
    return data


MM_TO_PIXEL = {
    "X": 1,
    "Y": 1
}


def mm_to_pixel(mm, axis):
    return mm * MM_TO_PIXEL[axis]


def img_to_pil_image(img):
    """Returns the input image as instance of PIL.Image.
    Note that it swaps the color channels from BRG to RGB if input is an array."""
    if isinstance(img, Image.Image):
        return img
    elif isinstance(img, numpy.ndarray):
        return Image.fromarray(img[...,::-1])
    else:
        raise Exception("Input is neither a numpy array nor an image.")


def img_to_cv2_img(img):
    """Returns the input image as a numpy array.
    Note that it swaps the color channels from RGB to BRG if input is a PIL image."""
    if isinstance(img, numpy.ndarray):
        return img
    elif isinstance(img, Image.Image):
        return numpy.array(img)[...,::-1]
    else:
        raise Exception("Input is neither a numpy array nor an image.")
