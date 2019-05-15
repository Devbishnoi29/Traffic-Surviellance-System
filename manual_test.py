import tensorflow as tf
import cv2
import os
import feed_data
import matplotlib.pyplot as plt
import matplotlib.patches as patches
characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
def character_testing():
    pretrained = os.path.isdir('store')
    if(pretrained == False):
        print("Please train your model first")
        return -1
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph("store/my_model.meta")
        saver.restore(sess, tf.train.latest_checkpoint("store/"))
        input_x = tf.get_collection("input_x")[0]
        input_y = tf.get_collection("input_y")[0]
        resultOp = tf.get_collection("resultOp")[0]

        batch_x, batch_y, img_name_list = feed_data.fetchImageData() # list all images of chars from test_data folder
        batch_size = len(batch_x)
        # number of images
        result = sess.run(resultOp, feed_dict = {input_x: batch_x})
        resultidx = tf.argmax(result, 1)
        resultidx = sess.run(resultidx)
        for i in range(batch_size):
            print(img_name_list[i], "  predicted: ", characters[resultidx[i]])

#character_testing()
def vehicle_image_testing():
    pretrained = os.path.isdir('store')
    if(pretrained == False):
        print("Please train your model first")
        return -1

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph("store/my_model.meta")
        saver.restore(sess, tf.train.latest_checkpoint("store/"))
        input_x = tf.get_collection("input_x")[0]
        input_y = tf.get_collection("input_y")[0]
        resultOp = tf.get_collection("resultOp")[0]

        '''
        batch_x, batch_y, img_name_list = feed_data.fetchImageData()
        np_list, np_names = feed_data.fetchNpData()
        no_np = len(np_list)
        # number of images
        for i in range(no_np):
            result = sess.run(resultOp, feed_dict = {input_x: np_list[i]})
            resultidx = tf.argmax(result, 1)
            resultidx = sess.run(resultidx)
            print("number plate: ", np_names[i])
            for i in range(len(np_list[i])):
                print(characters[resultidx[i]] ,end = ' ')
            print("\n")
        '''

        car_name = input("Enter car image name : ")
        img_path = "./indian_cars/" + car_name
        list_chars,gray_image,min_row,min_col,max_row,max_col = feed_data.fetchNpData(img_path)
        #Number of characters belong to single number plate
        if(len(list_chars) == 0):
            print("No valid found")
            exit()
        result = sess.run(resultOp, feed_dict = {input_x: list_chars})
        
        '''
        Experiment Don't uncomment it
        size = len(result)
        limit = size-4
        tmp= -1
        idx =0
        for i in range(size):
            if( i <= 1):
                for j in range(10,36,1):
                    if(result[i][j] > tmp):
                        tmp = result[i][j]
                        idx = j
                #resultidx[i] = idx
            elif ( i==2 or i==3):
                for j in range(0,10,1):
                    if(result[i][j] > tmp):
                        tmp = result[i][j]
                        idx = j
                #resultidx[i] = idx
            elif ( i >= limit):
                for j in range(0,10,1):
                    if(result[i][j] > tmp):
                        tmp = result[i][j]
                        idx = j
                #resultidx[i] = idx
            elif ( i == 4):
                for j in range(10,36,1):
                    if(result[i][j] > tmp):
                        tmp = result[i][j]
                        idx = j
                #resultidx[i] = idx

            for j in range(len(result[i])):
                if j != idx :
                    result[i][j]=0
                    '''
        resultidx = tf.argmax(result, 1)
        resultidx = sess.run(resultidx)
        print("#########################################\n")
        print("Number Plate Characters:    ", end=" ")
        ans = ""
        for i in range(len(resultidx)):
            print(characters[resultidx[i]] ,end = '')
            ans += characters[resultidx[i]]

        print("\n\n#########################################\n")
        fig, (ax1) = plt.subplots(1)
        ax1.imshow(gray_image, cmap="gray")
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False,label=ans)
        ax1.add_patch(rectBorder)
        plt.legend()
        plt.show()
vehicle_image_testing()
