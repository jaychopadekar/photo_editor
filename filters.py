import cv2
import numpy as np

def apply_filter(image, filter_name):
    if filter_name == "Grayscale":
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif filter_name == "Sepia":
        # Apply a sepia filter
        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        sepia_image = cv2.transform(image, sepia_filter)
        return np.clip(sepia_image, 0, 255).astype(np.uint8)
    elif filter_name == "Negative":
        # Apply a negative filter (invert colors)
        return cv2.bitwise_not(image)
    else:
        return image