import cv2
import numpy as np
import math
from skimage.filters import threshold_otsu

# module level variables ##########################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

###################################################################################################
def preprocess(imgGrayscale):
    #imgGrayscale = extractValue(imgOriginal)

    #cv2.imshow("imgGrayscale", imgGrayscale)
    #cv2.waitKey(0)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)
    #cv2.imshow("imgMaxContrastGrayscale", imgMaxContrastGrayscale)
    #cv2.waitKey(0)

    height, width = imgGrayscale.shape
    _, imgThresh = cv2.threshold(imgMaxContrastGrayscale, 127, 255, cv2.THRESH_BINARY)
    #imgThresh = cv2.adaptiveThreshold(imgMaxContrastGrayscale, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    cntw = 0
    cntb = 0
    flag = False
    for i in range(height):
        for j in range(width):
            if(imgThresh[i][j]):
                cntw += 1
            else:
                cntb += 1
    if(cntw < cntb):
        flag = True
    return flag
# end function


def gray_to_thresh(imgGrayscale):
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)
    height, width = imgGrayscale.shape
    _, imgThresh = cv2.threshold(imgMaxContrastGrayscale, 127, 255, cv2.THRESH_BINARY)
    return imgThresh
# end function

###################################################################################################
def maximizeContrast(imgGrayscale):

    height, width = imgGrayscale.shape

    imgTopHat = np.zeros((height, width, 1), np.uint8)
    imgBlackHat = np.zeros((height, width, 1), np.uint8)

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat
# end function