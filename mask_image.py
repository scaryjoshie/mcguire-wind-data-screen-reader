# Imports
import cv2
import numpy as np

# Mask Image Function
def MaskImage(im):

    # Converts PIL image to opencv image
    cvImage = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

    # Creates masks
    #mask1 = np.array([130, 108, 109])
    mask1 = np.array([0, 0, 0])
    #mask2 = np.array([206, 190, 171])
    mask2 = np.array([220, 230, 190])
    
    # Applies masks
    mask = cv2.inRange(cvImage, mask1, mask2)
    mask = 255-mask
    masked_image = cv2.bitwise_and(cvImage,cvImage, mask=mask)

    # Converst to grayscale
    grayImage = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    # Returns masked image
    return blackAndWhiteImage