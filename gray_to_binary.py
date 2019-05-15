from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import cv2
import numpy as np

def gray_to_binary(image_path):
	test_image_path = image_path  #"./indian_cars/car31.jpg"
	gray_car_image = cv2.imread(test_image_path, 0) 	# read the file in grayscale

	#cv2.imshow('Original Image: ', car_image);		#show the original image
	#cv2.waitKey(0)
	gray_image = imread(test_image_path, as_grey=True)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.imshow(gray_image,cmap="gray")			#Show Grayscale image of car on one side
	threshold_value = threshold_otsu(gray_image)	#finding the threshold value for the GrayScale Image
	#??? 	Try to understand the functioning of function threshold_otsu 


	binary_car_image = gray_image > threshold_value	#converting the grayscale to binary image
	ax2.imshow(binary_car_image, cmap="gray")		#Show Binary Image on the other side.
	plt.show()
	return binary_car_image, gray_car_image

def gray2binary(img):
	gray_image = img / 255
	threshold_value = threshold_otsu(gray_image)
	binary_car_image = gray_image > threshold_value
	return binary_car_image