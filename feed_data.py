# Programmer : Dev Bishnoi

import csv
import numpy as np
import os
import cv2
import image_processing as ip
import segmentation as seg
import connected_component as cc

def fetchData(reader, batch_size):
	cnt = 1
	images = []
	labels = []
	for row in reader:
		idx = int(row[0])
		label = np.zeros([36])
		#idx = idx - 1
		label[idx] = 1
		img = row[1:]
		image = [np.float32(x) for x in img]
		images.append(image)
		labels.append(label)
		if(cnt == batch_size):
			break
		cnt += 1
	return images, labels

test_path = './test_data1'

def fetchImageData():
    img_list = os.listdir(test_path)
    print(len(img_list))
    labels=[]
    imglist=[]
    img_name_list = []
    for img in img_list:
        labels.append(img[0:1])
        img_name_list.append(img)
        image = cv2.imread(test_path + "/" + img, 0)
        flag = ip.preprocess(image)
        if(flag):
            print("reveresed img : ", img)
            image = 255 - image
        image = cv2.resize(image, (28,28))
       	image = image.flatten()
        imglist.append(image)
    return imglist, labels, img_name_list

'''
	for i in range(len(label)):
        print(label[i])
        cv2.imshow(str(label[i]),imglist[i])
        cv2.waitKey(0)
'''

np_path = './Number Plates'
def fetchNpData(imgpath):
	npimg,gray_image,min_row,min_col,max_row,max_col = cc.cca(imgpath)
	#npimg = cv2.imread('./Number Plates/' + npname, 0)
	#print("returned image shape and data type : ", npimg.shape, type(npimg))
	npimg = npimg * 255
	img = np.array(npimg, dtype=np.uint8)
	#cv2.imshow("retured image", img)
	#cv2.waitKey(0)
	resized_img = cv2.resize(img, (250, 60))
	#print("image gathered from manish module ")
	char_list = seg.segmentation(resized_img)
	return char_list,gray_image,min_row,min_col,max_row,max_col