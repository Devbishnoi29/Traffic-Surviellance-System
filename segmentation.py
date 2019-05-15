# Programmers : Dev Bishnoi
import cv2
import numpy as np
import image_processing as ip
import noise_removal as nrm
mov_x = [0, 0, 1, -1]
mov_y = [1, -1, 0, 0]


mx = 0
mn = 100000
mnx = 100000
mxx = 0
def dfs(visit, x, y, h, w, img):
	global mn, mx, mxx, mnx
	if(mn > y):
		mn = y
	if(mx < y):
		mx = y
	if(mnx > x):
		mnx = x
	if(mxx < x):
		mxx = x
	visit[x][y] = 1
	for i in range(4):
		next_x = x + mov_x[i]
		next_y = y + mov_y[i]
		if( next_x < h and next_y < w and next_x and next_y and visit[next_x][next_y] == 0 and img[next_x][next_y]<255):
			dfs(visit, next_x, next_y, h, w, img)



def segmentation(img):
	global mx, mn, mnx, mxx
	img = nrm.remove_noise(img)
	"""
	print("back to segmentation function ")
	cv2.imshow("noise removed image4 " ,img2)
	cv2.waitKey(0)
	"""


	h, w = img.shape
	visit = np.zeros((h, w), np.int)
	mx = 0
	mn = w
	chr_list = []
	j = 10
	while(j < w - 4):
		if(img[int(h/2)][j]<255):
			mn = j
			mx = j
			mxx = int(h/2)
			mnx = mxx
			dfs(visit, int(h/2), j, h, w, img)

			crop_img = img[2:h-2, mn - 2:mx + 2]

			height = mxx - mnx
			width = mx - mn

			ht_frac = height/h
			wt_frac = width/w
			
			if(height < width or ht_frac>0.8 or ht_frac<0.4 or wt_frac < 0.03 or wt_frac > 0.1 or crop_img.shape[0] == 0 or crop_img.shape[1] == 0):
				print("invalid character")
			else:
				#cv2.imshow("croped img" ,crop_img)
				#cv2.waitKey(0)
				crop_img = cv2.resize(crop_img, (28, 28))
				#cv2.imshow("crop and resized image" ,crop_img)
				#cv2.waitKey(0)
				flatten = crop_img.flatten()
				chr_list.append(flatten)
			#print("factions width and height", wt_frac, " ", ht_frac)
			j = mx
			#print("\n")
		#print("j: ", j)
		j += 1
	return chr_list