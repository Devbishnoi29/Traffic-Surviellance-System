# Programmer : Dev Bishnoi

# This file contains multiple function to preprocess datasets provided. Use appropriate function according to your requirement.
# If you are running first method then make comment to another one.

import csv
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
import os
import noise_removal as nrm

'''
mov_x = [0, 0, 1, -1]
mov_y = [1, -1, 0, 0]

#file_write = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist-0A/data.csv", 'w', newline='')
#writer = csv.writer(file_write, delimiter=',')


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



def seg(img):
	global mx, mn, mnx, mxx
	#img = cv2.imread("Number Plates/" + np_name, 0)
	img = nrm.remove_noise(img)

	h, w = img.shape
	visit = np.zeros((h, w), np.int)
	mx = 0
	mn = w
	chr_list = []
	j = 4
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
			#print("imgshape " , crop_img.shape)
			#print(crop_img)
			if(height < width or ht_frac>0.8 or ht_frac<0.4 or wt_frac < 0.03 or wt_frac > 0.1):
				print("invalid character")
			elif ( crop_img.shape[0] == 0 or crop_img.shape[1] == 0):
				print('I am devil')
			else:
				print("wow")
				#cv2.imshow("croped img" ,crop_img)
				#cv2.waitKey(0)
				crop_img = cv2.resize(crop_img, (28, 28))
				#cv2.imwrite('tryChar.png',crop_img)
				#crop_img = cv2.imread('./tryChar.png',0)
				cv2.imshow("croped img" ,crop_img)
				cv2.waitKey(200)
				flat = crop_img.flatten()
				label_val = int(input("Enter label: "))
				im = [label_val]
				for i in range(784):
					im.append(flat[i])
				writer.writerow(im)
			j = mx
			print("\n")
		j += 1
	return# chr_list

np_path = './Number Plates'

def numberplate_to_csv():
	npimgs = os.listdir(np_path)
	for imgname in npimgs:
		npimg = cv2.imread( np_path + '/' + imgname, 0)
		npimg = cv2.resize(npimg, (240, 50))
		seg(npimg)


#numberplate_to_csv()

#######################################################################################################################
#before using this script please have a look on this file.
file_read = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist/data.csv", 'r')
file_write = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist-0A/test.csv", 'w', newline='')
reader = csv.reader(file_read, delimiter=',')
writer = csv.writer(file_write, delimiter=',')

# It extract digits and capital alphabet letters from emnist-balanced-train.csv into emnist_train.csv.
def extract():
	cnt = 0
	for row in reader:
		cnt += 1
		label = int(row[0])
		if(label <= 35):
			writer.writerow(row)
extract()

'''
########################################################################################################################


# Just to visualize data, weather they are correctly processed or not.
file_read = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist-0A/captured_data.csv", 'r')
reader = csv.reader(file_read, delimiter=',')

def showData():
	cnt = 0
	for row in reader:
		cnt += 1
		idx = row[0]
		img = row[1:]
		image = [int(x) for x in img]
		image_file = np.reshape(image, [28, 28])
		cv2.imwrite( "./test_data1/"+idx + "_" + str(cnt) + ".jpg", image_file)
showData()

'''

###############################################################################################################################

# Flip vertically and then rotate by 90 degree anti-clock-wise.
# Image is being loaded from emnist_train.csv and then processed (flipped and rotated ) image is written to train.csv
fread = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist-0A/emnist_train.csv", 'r')
fwrite = open("C:/Users/Devilal/Documents/Machine Learning/Data/emnist-0A/train.csv", 'w', newline='')
reader = csv.reader(fread, delimiter=',')
writer = csv.writer(fwrite, delimiter = ',')
def preprocess():
	for row in reader:
		img = row[1:]
		image = np.reshape(img, [28, 28])
		for i in range(28):
			for j in range(28):
				if(i > j):
					item = image[i][j]
					image[i][j] = image[j][i]
					image[j][i] = item
		image = np.reshape(image, [28 * 28])
		l = len(image)
		for i in range(l):
			row[i+1] = image[i]
		writer.writerow(row)
preprocess()
'''
