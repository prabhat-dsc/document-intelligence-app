

import cv2
import numpy as np 

def preprocess_image(pil_image, mode : str = "document"):
    image = np.array(pil_image.convert("RGB"))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if mode == "low_contrast":
        gray = cv2.equalizeHist(gray)

    # Mild denoising preserves text better than aggressive filtering.
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Otsu works well for many clean scans. Keep the original grayscale
    # available because some documents are harmed by thresholding.

    _, thresholded = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresholded



