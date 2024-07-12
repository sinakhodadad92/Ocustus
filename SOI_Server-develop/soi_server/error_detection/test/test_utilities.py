import unittest
from error_detection.utilities import *
from PIL import Image
import cv2
import numpy as np


class MyTestCase(unittest.TestCase):
    def test_img_to_pil_image(self):
        image_path = "error_detection/test/test_board_images/board_1.jpg"
        pil_image = Image.open(image_path, )
        array_image = cv2.imread(image_path)
        self.assertEqual(img_to_pil_image(pil_image), pil_image)
        self.assertTrue(pil_image.size[0] > 0 and array_image.shape[0] > 0)
        # use np.array for comparison because of different subtypes of PIL Image
        #self.assertTrue(np.allclose(np.array(img_to_pil_image(array_image)), np.array(pil_image)))

    def test_img_to_array(self):
        image_path = "error_detection/test/test_board_images/board_1.jpg"
        pil_image = Image.open(image_path)
        array_image = cv2.imread(image_path)
        # self.assertTrue(np.allclose(img_to_cv2_img(array_image), array_image))
        # self.assertTrue(np.allclose(img_to_cv2_img(pil_image), array_image))


if __name__ == '__main__':
    unittest.main()
