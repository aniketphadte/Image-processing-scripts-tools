#Script to crop images and turn it to gray scale for creating an image processing model
#Instructions to use the code
#1> Drag andselect the required path
#2> Press c to crop the image
#3> Press r to reset the image
#4> Press k to save the image
#5> Prese n from next image
#6> Press ESC to close the editing tool


import os
import cv2
import argparse

#Original image paths
pathPosRaw = "D:\\pythonFiles\\rawData\\positive\\"
pathNegRaw = "D:\\pythonFiles\\rawData\\negative\\"
#Destination paths to save the images
pathPos ="D:\\pythonFiles\\positive\\"
pathNeg ="D:\\pythonFiles\\negative\\"

#height and width of the positive image
max_pos_width = 100
max_pos_height = 100
#height and width of the negative image
max_neg_width = 200
max_neg_height = 200
refPt =[]
croping = False;
#image = cv2.imread(null)


def click_and_crop(event, x,y, flags, param):
    global refPt, croping, image
    
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt =[(x,y)]
        croping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x,y))
        croping = False

        cv2.rectangle(image,refPt[0],refPt[1],(0,255,0), 2)
        cv2.imshow("fullImage", image)


#listing = os.listdir(pathPosRaw)
if not os.path.exists(pathPos):
    os.makedirs(pathPos)
if not os.path.exists(pathNeg):
    os.makedirs(pathNeg)



def get_images(path_raw,save_path, max_width,max_height):
    global image
    listing = os.listdir(path_raw)
    for file in listing:
        image = cv2.imread(path_raw+file)
        width_main, height_main = image.shape[:2]
        if(width_main > 1024 or height_main > 720):
            image = cv2.resize(image,(800,600))
        clone = image.copy()
        pic_num =1
        cv2.namedWindow("fullImage")
        cv2.setMouseCallback("fullImage",click_and_crop)
        while True:
            cv2.imshow('fullImage', image)
            key = cv2.waitKey() & 0xFF
            print(str(pic_num))

            if key == ord("r"):
                image = clone.copy()

            elif key==ord("c"):
                if len(refPt) == 2:
                    roi = clone[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0]]
                    cv2.imshow("ROI", roi)
                    save_key = cv2.waitKey() & 0xFF
                    print(save_key)
                    if save_key == ord("k"):
                        save_img = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
                        cv2.imshow("save Image", save_img)
                        width, height = save_img.shape
                        print(str(width) + " " + str(height))
                        if(width > max_width or height > max_height):
                            resized_img = cv2.resize(save_img,(max_width,max_height))
                            cv2.imwrite(save_path+file.split('.',1)[0]+str(pic_num) +".jpg", resized_img)
                        else:
                            cv2.imwrite(save_path+file.split('.',1)[0]+str(pic_num) +".jpg", save_img)
                            
                    
            elif key==ord("n"):
                break
            if key == 27 :
                break
            pic_num +=1

        if key==27 :
            break

#resize the whole image       
def resize_neg_save(path_raw,save_path, max_width,max_height):
    global image
    listing = os.listdir(path_raw)
    i=0
    for file in listing:
        image = cv2.imread(path_raw+file)
        pic_num =100
        cv2.namedWindow("fullImage")
        i=i+1
        print(i)
        width, height = image.shape[:2]
        if(width > 1024 or height > 720):
            resized_main_img = cv2.resize(image,(800,600))
            cv2.imshow('fullImage', resized_main_img)
            save_img = cv2.cvtColor(resized_main_img, cv2.COLOR_RGB2GRAY)
            resized_img = cv2.resize(save_img,(max_width,max_height))
            cv2.imwrite(save_path+file.split('.',1)[0]+str(pic_num) +".jpg", resized_img)
        else:
            cv2.imshow('fullImage', image)
            save_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            resized_img = cv2.resize(save_img,(max_width,max_height))
            cv2.imwrite(save_path+file.split('.',1)[0]+str(pic_num) +".jpg", save_img)
        if i%100== 0:
            cv2.destroyAllWindows()


get_images(pathPosRaw, pathPos, max_pos_width, max_pos_height )
#get_images(pathNegRaw, pathNeg, max_neg_width, max_neg_height )
#To resize the whole image
#resize_neg_save(pathNegRaw, pathNeg, max_neg_width, max_neg_height )

cv2.destroyAllWindows()
    
    
