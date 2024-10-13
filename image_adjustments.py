import cv2
import numpy as np

def adjust_brightness(image, brightness=0):
    return cv2.convertScaleAbs(image, beta=brightness)

def adjust_contrast(image, contrast=0):
    alpha = contrast / 100 + 1.0  # Contrast control
    return cv2.convertScaleAbs(image, alpha=alpha)

def adjust_saturation(image, saturation=100):
    # Convert the image to HSV (Hue, Saturation, Value)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)

    h, s, v = cv2.split(hsv_image)
    s = s * (saturation / 100.0)
    s = np.clip(s, 0, 255)

    # Merge channels and convert back to RGB
    hsv_image = cv2.merge([h, s, v])
    final_image = cv2.cvtColor(hsv_image.astype(np.uint8), cv2.COLOR_HSV2RGB)

    return final_image

def sharpen_image(image):
    # Define the sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    # Apply the kernel to the image
    sharpened = cv2.filter2D(image, -1, kernel)
    return sharpened


def denoise_image(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)