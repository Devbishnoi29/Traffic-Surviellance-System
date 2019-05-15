import numpy as np
import cv2
import image_processing as ip
import gray_to_binary as gtb

mov_x = [0, 0, 1, -1]
mov_y = [1, -1, 0, 0]

def dfs(x, y, visit, imgb, h, w):
	visit[x][y] = 1
	for idx in range(4):
		next_x = x + mov_x[idx]
		next_y = y + mov_y[idx]
		if(next_y < w and next_x < h and next_x and next_y and imgb[next_x][next_y]==0 and visit[next_x][next_y] == 0):
			dfs(next_x, next_y, visit, imgb, h, w)


def remove_noise(img):
	#Reverse image if it is not as per standerds
	flag = ip.preprocess(img)
	if(flag):
		img = 255 - img

	imgb = ip.gray_to_thresh(img)
	'''img2 = gtb.gray2binary(img)
	img2 = img2 * 255
	cv2.imshow("binary image before noise removal step1 ", imgb)
	cv2.waitKey(0)
	'''
	h, w = imgb.shape

	visit = np.zeros((h, w), dtype = np.int)

	for j in range(4, w-4):
		if(imgb[int(h/2)][j]==0 and visit[int(h/2)][j] == 0):
			dfs(int(h/2), j, visit, imgb, h, w)

	for i in range(h):
		for j in range(w):
			if(visit[i][j] == 0):
				img[i][j] = 255
				imgb[i][j] = 255

	#cv2.imshow("binary image after noise removal step2 ", imgb)
	#cv2.waitKey(0)
	cv2.imshow("gray image after noise removal step3 ", img)
	cv2.waitKey(0)
	return img
