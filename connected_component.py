from skimage import measure
from skimage import restoration
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gray_to_binary as gb
import cv2
from skimage.filters import threshold_otsu
import numpy as np
import os

#Called function "cca" from outside
def eliminate_bogus_plate(candidates):
    #This function will try to eliminate the Invalid candidates of the Number Plate
    license_plate=[]
    fraction_black=[]
    for cand in candidates:
        ht,wd = cand.shape
        cntw=0
        cntb=0
        #fig, ax1 = plt.subplots(1)
        #ax1.imshow(cand, cmap="gray")
        for i in range(ht):
            for j in range(wd):
                if cand[i][j] == True:
                    cntw +=1
                else:
                    cntb +=1
        #print('black: ',cntb,' white :',cntw)
        percentage = (float(cntb)/float(cntw))
        #print('percentage :',percentage)
        # WE MADE AN OBSERVATION THAT (FOREGROUND/BACKGROUND)*100 <= 60 ,FOR VALID NUMBER PLATES 
        #if percentage <= 50:                        #BASED ON MY PERSONAL EXPERIENCE AND ANALYSIS.
        if percentage <= 0.68:                         # Car 12 was giving wrong for 50 percentage
            license_plate.append(cand)
            fraction_black.append(percentage)
    idx = 0
    tmp = 10000000
    for i in range(len(license_plate)):
        if(fraction_black[i] < tmp ):
            tmp = fraction_black[i]
            idx = i
    if(len(license_plate) <= 0 ):
        print('No plate detected')
        plt.show()
        exit()
    valid_plate = license_plate[idx]
    #plt.show()
    return valid_plate

def enhanceImage(img):
    #This function enhances the image by changing the intensity of a pixel below a certain level
    #find the min intensity value in image( possible that is of character in number plate)
    ht,wd = img.shape
    for i in range(ht):
        for j in range(wd):
            if(img[i][j] > 100 and img[i][j] < 160 ):
                img[i][j] = 240
    return img

def cca(image_path):
    # this gets all the connected regions and groups them together
    # all the pixels having same intensity
    (binary_image, gray_image) = gb.gray_to_binary(image_path)
    #cv2.imshow('original:',gray_image)
    label_image = measure.label(binary_image)

    #???  Understand the functioning of 'label' function.


    # getting the maximum width, height and minimum width and height that a license plate can have.
    # plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
    # BECAUSE THE LENGTH AND WIDTH OF THE NUMBER PLATE ARE SPECIFIED BY GOVERNMENT.
    plate_dimensions = (0.06*label_image.shape[0], 0.12*label_image.shape[0], 0.18*label_image.shape[1], 0.40*label_image.shape[1])
    
    #plate_dimensions = (0.03*label_image.shape[0], 0.15*label_image.shape[0], 0.18*label_image.shape[1], 0.40*label_image.shape[1])

    min_height, max_height, min_width, max_width = plate_dimensions

    plate_objects_cordinates = []
    plate_like_objects = []                 #ALL the Possible Candidates for the Number_Plate, Only one will be valid.

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_image, cmap="gray");

    # regionprops creates a list of properties of all the labelled regions(ALL THE CONNECTED AREAS)
    for region in regionprops(label_image):
        if region.area < 50:
            #if the region is so small then it's likely not a license plate
            continue

        # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        region_height = max_row - min_row
        region_width = max_col - min_col
        # ensuring that the region identified satisfies the condition of a typical license plate
        #if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        #if region_height >= min_height and region_width >= min_width and region_width > region_height:
        # BECAUSE SIZE OF NUMBER PLATE IS SPECIFIED BY GOVERNMENT, SO WE CAN USE SOME ASSUMPTIONS TO ELIMINATE INVALID PLATES.
        if region_width > region_height and region_height >= min_height and region_width >= min_width and region_height <= max_height and region_width <= max_width:
            plate_like_objects.append(binary_image[min_row:max_row, min_col:max_col])
            #plate_like_objects.append(gray_image[min_row:max_row, min_col:max_col])
            # Below lines are just for plotting Red box around the possible plates.
            plate_objects_cordinates.append((min_row, min_col, max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
            ax1.add_patch(rectBorder)

    plt.show()

    #print(len(plate_like_objects))
    #only 1 plate is returned
    valid_plate = eliminate_bogus_plate(plate_like_objects)
    idx =-1
    ht = valid_plate.shape[0]
    wd = valid_plate.shape[1]
    for i in range(len(plate_like_objects)):
        flag= True
        curH = plate_like_objects[i].shape[0]
        curW = plate_like_objects[i].shape[1]
        if( curH != ht or curW != wd):
            continue
        for j in range(ht):
            for k in range(wd):
                if valid_plate[j][k] != plate_like_objects[i][j][k] :
                    flag= False
        if(flag == True):
            idx= i
            break

    valid_plate = enhanceImage(valid_plate)
    min_row,min_col,max_row,max_col = plate_objects_cordinates[idx]

    return valid_plate,gray_image,min_row,min_col,max_row,max_col

#cca("./indian_cars/car1p.jpg")
#path = "./indian_cars/car8.jpg"
#path2 = "./Camera_2/"
#plate =cca(path)
#bi, gi = gb.gray_to_binary(path2)
#gi = cv2.imread(path2, 0)
#cv2.imshow('original ',gi)
#cv2.waitKey(0)
#img = enhanceImage(gi)#cca(path)
#cv2.imshow('enhanced ',img)
#cv2.waitKey(0)

