from collections import Counter

import cv2
import imagehash
import numpy as np
from sklearn.cluster import SpectralClustering

from error_detection.utilities import img_to_cv2_img, img_to_pil_image

"""
This file contains the algorithms to detect erroneous components.
"""


def get_sift_descriptors(img):
    detector = cv2.SIFT_create()
    return detector.detectAndCompute(img, None)[1]  # (keypoints, descriptors)


def sift_similarity(descriptors1, descriptors2):
    """
    Takes two images and computes a similarity value based on matching descriptors from the SIFT algorithm.
    Note that it's not an actual similarity since it's not symmetric. 
    """
    if descriptors1 is None or descriptors2 is None:
        return 0
    # -- Step 2: Matching descriptor vectors with a BF based matcher
    matcher = cv2.BFMatcher()
    # alternatively approximate matcher: DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
    # -- Filter matches using the Lowe's ratio test
    ratio_thresh = 0.75
    good_matches = []
    try:
        for m, n in knn_matches:
            if m.distance < ratio_thresh * n.distance:
                good_matches.append(m)
    except ValueError as e:
        return 0

    if len(knn_matches) == 0:
        return 0
    ld1, ld2 = len(descriptors1), len(descriptors2)
    return min(ld1, ld2)/max(ld1, ld2) * len(good_matches) / ld1


def get_canny_edges(image, low_thresh, high_thresh):
    img = img_to_cv2_img(image)
    return cv2.Canny(img, low_thresh, high_thresh)


def has_suspicious_hash(components, img_hash=imagehash.phash, threshold=28):
    """
    Checks whether among the given images there is a pair of images
    whose hash values have a difference greater or equal to the given threshold.
    Note that the hash function must map similar images to similar values in case it is exchanged."""
    low_thresh = 44
    high_thresh = 197
    for i in range(len(components)):
        for j in range(len(components)):
            if i < j:
                image_1 = img_to_pil_image(get_canny_edges(
                    components[i]['img'], low_thresh, high_thresh))
                image_2 = img_to_pil_image(get_canny_edges(
                    components[j]['img'], low_thresh, high_thresh))
                if threshold <= (img_hash(image_1) - img_hash(image_2)):
                    return True
    return False


def sift_similarity_symm(img1, img2):
    """
    Symmetric similarity measure by averaging sift_similarity for both orderings.
    """
    return (sift_similarity(img1, img2) + sift_similarity(img2, img1)) / 2


def get_similarity_matrix(components, callback=sift_similarity_symm):
    """
    Computes the similarity matrix for an array of images. sift_similarity_symm is used as default similarity measure.
    """
    similarity_matrix = np.identity(
        len(components))  # init with identity matrix, since diagonal is always one
    descriptors = []  # get all image descriptors
    for component in components:
        descriptors.append(get_sift_descriptors(
            img_to_cv2_img(component['img'])))

    for i in range(len(descriptors)):
        for j in range(len(descriptors)):
            if i < j:
                similarity_matrix[i, j] = callback(
                    descriptors[i], descriptors[j])
                similarity_matrix[j, i] = similarity_matrix[i, j]

    return similarity_matrix


def get_clustering(components, n_clusters=2, random_state=0):
    """
    Computes the spectral clustering for an array of images.
    For error detection n_clusters=2 should yield a cluster for correct and erroneous components each.
    The result is an array with the element index corresponding to the image index and the array values corresponding to
    the number of the cluster.
    """
    similarity_matrix = get_similarity_matrix(components)

    clustering = SpectralClustering(n_clusters=n_clusters,
                                    assign_labels='discretize',
                                    random_state=random_state,
                                    affinity='precomputed').fit(similarity_matrix)
    return clustering.labels_


def get_error_image_indices(clustering):
    """
    Returns all indices of presumably erroneous component images.
    Assumptions:
    - The largest cluster contains the correct components (if contains the majority of images)
    - if there is a tie which cluster is the largest, all indices are returned,
      i.e. we don't know where the error is, so everything has to be considered manually
    - some clustering algorithms consider noise, marked as -1, so a valid cluster id is non-negative
    """
    if len(clustering) == 0:
        return []

    # list of pairs where first element is id and second is frequency
    cluster_sizes = Counter(clustering).most_common()

    if cluster_sizes[0][0] < 0:  # not a cluster but noise if label < 0
        # all images are possibly erroneous
        return list(range(len(clustering)))
    # tie
    if len(cluster_sizes) > 1 and cluster_sizes[0][1] == cluster_sizes[1][1]:
        return list(range(len(clustering)))
    else:
        if cluster_sizes[0][1] <= len(clustering) / 2:  # check majority
            return list(range(len(clustering)))
        else:
            # filter for all indices that point to a elements not contained in the largest cluster
            return [i for i in range(len(clustering)) if clustering[i] != cluster_sizes[0][0]]


def error_detection(component_dict):
    print("Detect erroneous components\n")

    errors_dict = {}
    for component_designator in component_dict:

        if has_suspicious_hash(component_dict[component_designator]):

            clustering = get_clustering(component_dict[component_designator])
            error_indices = get_error_image_indices(clustering)
            for error_index in error_indices:
                error_component = component_dict[component_designator][error_index]
                if component_designator not in errors_dict:
                    errors_dict[component_designator] = []
                errors_dict[component_designator].append(error_component)

    return errors_dict
