import unittest
from error_detection.image_diff import *
import os


class ImageDiffTests(unittest.TestCase):
    img_correct1 = None
    img_correct2 = None
    img_error_1 = None
    img_error_2 = None
    base_path = ""

    def setUp(self) -> None:
        self.base_path = os.getcwd()
        self.img_correct_1 = cv2.imread(self.base_path + "/error_detection/test/test_component_images/flipped/1.jpg")
        self.img_correct_2 = cv2.imread(self.base_path + "/error_detection/test/test_component_images/flipped/2.jpg")
        self.img_error_1 = cv2.imread(self.base_path + "/error_detection/test/test_component_images/flipped/error1.jpg")
        self.img_error_2 = cv2.imread(self.base_path + "/error_detection/test/test_component_images/flipped/error2.jpg")

    def test_sift_similarity(self):
        """Test whether correct components have a greater similarity with each other than with erroneous ones.
        (Note that in exceptional cases this does not always hold) """

        self.assertGreater(
            sift_similarity(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_correct_2)),
            sift_similarity(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_error_1)))
        self.assertGreater(
            sift_similarity(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_correct_2)),
            sift_similarity(get_sift_descriptors(self.img_correct_2), get_sift_descriptors(self.img_error_1)))
        self.assertGreater(
            sift_similarity(get_sift_descriptors(self.img_correct_2), get_sift_descriptors(self.img_correct_1)),
            sift_similarity(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_error_2)))
        self.assertGreater(
            sift_similarity(get_sift_descriptors(self.img_correct_2), get_sift_descriptors(self.img_correct_1)),
            sift_similarity(get_sift_descriptors(self.img_correct_2), get_sift_descriptors(self.img_error_2)))

        """Test that equal images yield 1"""
        self.assertEqual(sift_similarity(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_correct_1)), 1)

    def test_sift_similarity_symm(self):
        """Test symmetry property """
        self.assertEqual(sift_similarity_symm(get_sift_descriptors(self.img_correct_1), get_sift_descriptors(self.img_correct_2)),
                         sift_similarity_symm(get_sift_descriptors(self.img_correct_2), get_sift_descriptors(self.img_correct_1)))
        self.assertEqual(sift_similarity_symm(get_sift_descriptors(self.img_error_2), get_sift_descriptors(self.img_error_1)),
                         sift_similarity_symm(get_sift_descriptors(self.img_error_1), get_sift_descriptors(self.img_error_2)))

    def test_get_clustering(self):
        test_cases_dict = self.get_clustering_test_images()
        for test_case_name in test_cases_dict.keys():
            print("Test clustering on " + test_case_name)
            test_case = test_cases_dict[test_case_name]
            images = test_case["error"] + test_case["correct"]
            clustering = get_clustering(images, n_clusters=2, random_state=1)
            first_cluster_id = clustering[0]
            for i in range(len(images)):
                 self.assertTrue(clustering[i] == first_cluster_id and i < len(test_case["error"])
                                 or clustering[i] != first_cluster_id and i >= len(test_case["error"]))

    def get_clustering_test_images(self):
        path = self.base_path + "/error_detection/test/test_component_images/"
        test_cases_dict = {}
        test_cases_names = os.listdir(path)
        for test_case_name in test_cases_names:
            if test_case_name == "correct":  # does not contain false images
                print("skip correct case")
            else:
                test_images = os.listdir(path + test_case_name)
                test_case = {"error": [], "correct": []}
                for img_name in test_images:
                    img = cv2.imread(path + test_case_name + "/" + img_name)
                    if img_name.find("error") >= 0:
                        test_case["error"].append({"img": img})
                    else:
                        test_case["correct"].append({"img": img})
                test_cases_dict[test_case_name] = test_case
        return test_cases_dict

    def test_get_error_image_indices(self):
        clustering_empty = []
        clustering_invalid = [-1, -1, -1, -1]
        clustering_valid_1 = [-1, -1, -1, 1, 1, 1, 1]
        clustering_valid_2 = [2, 2, 2, 2, 1, 1, 1]
        clustering_no_errors = [0, 0, 0, 0]
        clustering_tie = [1, 1, 2, 2]
        self.assertEqual(get_error_image_indices(clustering_empty), [])
        self.assertEqual(get_error_image_indices(clustering_invalid), [0, 1, 2, 3])
        self.assertEqual(get_error_image_indices(clustering_valid_1), [0, 1, 2])
        self.assertEqual(get_error_image_indices(clustering_valid_2), [4, 5, 6])
        self.assertEqual(get_error_image_indices(clustering_no_errors), [])
        self.assertEqual(get_error_image_indices(clustering_tie), [0, 1, 2, 3])


if __name__ == '__main__':
    unittest.main()
