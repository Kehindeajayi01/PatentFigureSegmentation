import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
import glob


"""
This function takes in the image path, process the image, detects the contours
in the image, save the image bounding boxes, and finds the distance between 
the image midpoints and the label centers.
"""

# path to the image
#path = "C:/Users/ajayi/OneDrive/Desktop/100patents_design_jpg/subfigures/*.jpg"
patent_imgs = "C:/Users/ajayi/OneDrive/Desktop/100patents_design_jpg/patent_images/*.jpg"

"""This function collects all the subfigure files"""
def get_files(file_path):
    files = glob.glob(file_path)
    return files

img_paths = get_files(patent_imgs)
# Image processing
def image_processing(index):
    
    img_path = img_paths[index]
    #args = get_args()
    image = cv2.imread(img_path)
    # Optional: resize the image
    image = cv2.resize(image, None, fx = 0.3, fy = 0.3, interpolation=cv2.INTER_AREA)

    # get the coordinates of the resized image: we will use it to convert the amazon recognition bounding
    # boxes converted coordinates
    h, w = image.shape[:2]

    # End goal: find contours, draw the bounding box around the contours, find minimum area enclosing the 
    # contours

    # convert to a grayscale image, and apply thresholding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the image to remove some noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # Use Canny edge detector to detect the edges
    edged = cv2.Canny(blurred, 50, 200)
    # dilate and erode the image to close any gaps in the edge detected
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    return image, edged, h, w


def image_contours(index):
    image, edged, h, w = image_processing(index)
    image_coord = []
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop through the contours
    for c in cnts:
        if cv2.contourArea(c) > 1000:
            # find the minimum area   
            rect = cv2.minAreaRect(c)
            # calculate the coordinates of the minimum area rectangle
            box = cv2.boxPoints(rect)
            # Convert the coordinates to integers
            box = np.int0(box)
            image_coord.append(np.abs(box))
        
            cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
        
    return image_coord 

# image midpoints calculation
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) / 2), ((ptA[1] + ptB[1]) / 2) 


def midpoints_image(image_coord):
    
    image_midpoints = list()
    
    # case for a single image
    if len(image_coord) == 1:
        tltrX, tltrY = midpoint(image_coord[0], image_coord[1])
        # midpoints btw bottom-left and bottom-right
        blbrX, blbrY = midpoint(image_coord[2], image_coord[3])
        # midpoints of both results
        mX, mY = midpoint((tltrX, tltrY), (blbrX, blbrY))
        image_midpoints.append((mX, mY))
    
    else:
        # case for image with subfigures
        # loop through the figure coordinates and get the midpoints
        for image in reversed(image_coord):
            # midpoints btw top-left and top-right 
            tltrX, tltrY = midpoint(image[0], image[1])
            # midpoints btw bottom-left and bottom-right
            blbrX, blbrY = midpoint(image[2], image[3])
            # midpoints of both results
            mX, mY = midpoint((tltrX, tltrY), (blbrX, blbrY))
            image_midpoints.append((mX, mY))
    
    return image_midpoints


# find the distance between the label coordinates and the image coordinates
def AmazonDist_label_image(label_cent, image_mid):
    D = {}
    # distance for a single image
    if len(image_mid) == 1 and len(label_cent) == 1:
        # calculate the distance between the label and image
        dist = round(distance.euclidean(label_cent[0], image_mid), 2)
        D['distance'] = dist
    else:  
        # distance for image with subfigures   
        # loop through the label coordinates and unpack the coordinates
        for ind1, lab in enumerate(label_cent):
        
            # loop through the image coordinates and unpack also
            for ind2, img in enumerate(image_mid):
            
                # calculate the distance between the label and image
                dist = round(distance.euclidean(lab, img), 2)
                D[(ind1, ind2)] = dist      
    
    return D
