import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
from scipy.spatial import distance
from segment_image import figure_only, draw_contour
from amazon_dist_calc import midpoint, midpoints_image
from amazon_dist_calc import AmazonDist_label_image

# function to find the center of the label coordinates
def calc_label_center(label_coord):
    label_cent = []
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
    
    return label_cent
    

image, label_coord = figure_only(0)
image_coord = draw_contour(0)
label_cent = calc_label_center(label_coord)
image_mid = midpoints_image(image_coord)
Dist = AmazonDist_label_image(label_cent, image_mid)

print(f"Distance: \n{Dist}")