import cv2
from error_detection.utilities import img_to_pil_image


def background_removal(img):
    print("Removing background\n")

    # (1) Convert to gray, and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV)

    # (2) Morph-op to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

    # (3) Find the max-area contour
    cnts = cv2.findContours(morphed, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv2.contourArea)[-1]

    # (4) Crop and return it
    x, y, w, h = cv2.boundingRect(cnt)
    dst = img[y:y+h, x:x+w]
    return img_to_pil_image(dst)

def background_removal_multi(panel_tuples):
    cropped_panels = []
    for panel_tuples in panel_tuples:
        cropped_panels.append({
            'id': panel_tuples[0],
            'img': background_removal(panel_tuples[1])
        })
    return cropped_panels
