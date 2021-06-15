import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
import glob
from Amazon_label import *
from amazon_test import *


# image midpoints calculation
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) / 2), ((ptA[1] + ptB[1]) / 2) 


def midpoints_image(index):
    
    image_midpoints = list()
    image_coord = draw_contour(index)
    try:
        
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
    except Exception as error:
        print(error)
    
    return image_midpoints


