import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
from scipy.spatial import distance
from amazon_test import figure_only, draw_contour
from amazon_dist_calc import midpoint, midpoints_image


# function to find the center of the label coordinates
def calc_label_center(index):
    label_cent = []
    label_coord, _ = figure_only(index)
    try:
        
        # case for a single image
        if len(label_coord) == 1:
            left, width, top, height = label_coord[0]
            # Obtain the center coordinates by adding the top to the height / 2, and adding left to width / 2
            ptX, ptY = (width / 2 + left), (height / 2 + top)
            # save it in the label_cent list
            label_cent.append((ptX, ptY))
        
        else:   
            # case for image with subfigures
            for coord in label_coord:
                left, width, top, height = coord
                # Obtain the center coordinates by adding the top to the height / 2, and adding left to width / 2
   
                ptX, ptY = (width / 2 + left), (height / 2 + top)
                # save it in the label_cent list
                label_cent.append((ptX, ptY))
    except Exception as error:
        print(error)
    
    return label_cent
    

# find the distance between the label coordinates and the image coordinates
def AmazonDist_label_image(index):
    D = {}
    label_cent = calc_label_center(index)
    image_mid =  midpoints_image(index)
    # distance for a single image
    try:
        
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
    except Exception as error:
        print(error)
    return D

