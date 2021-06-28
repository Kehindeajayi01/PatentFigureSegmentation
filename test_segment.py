from segmentation_pipeline import label_points, get_files
import cv2
import numpy as np
from Amazon_label import extract_label_bboxes
from amazon_test import *
import os
import string
import json
from Amazon_label import get_args
import argparse
import matplotlib.pyplot as plt


# This function loads the image and wipe out the labels 
# using label coordinates from Amazon Rekognition tool
def figure_only(index):
    try:
        
        # get patent id
        parser = get_args()
        args = parser.parse_args()
        amazon_paths = args.amazonDirectory
        output_dir = args.outputDirectory
        img_paths = get_files()
        img_dir = args.file_path
        rel_paths = os.listdir(img_dir)
        relative_path = rel_paths[index]
        img_path = img_paths[index]  # img_paths is from amazon_dist_calc
        image = cv2.imread(img_path)
        # resize the image
        image_res = cv2.resize(image, None, fx = 0.3, fy = 0.3, interpolation=cv2.INTER_AREA)
        #image, edged, h, w = image_processing()
        label_coord = label_points(index)  # this is from Amazon Rekognition tool
        # case for a single image
        if len(label_coord) == 1:
            # unpack the coordinates
            left, width, top, height = label_coord[0]
            # set the pixels in those location to zero
            image_res[(top) : (top + height), (left): (left + width)] = (255, 255, 255)
            label_coord = label_coord[0]
        
            cv2.imwrite(os.path.join(output_dir, relative_path), image_res)
        else:  
            # case for image with subfigures
            for label in label_coord:
                # unpack the coordinates
                left, width, top, height = label
                # set the pixels in those location to zero
                image_res[(top -1) : (top + height + 1), (left -1): (left + width + 1)] = (255, 255, 255)
            
            cv2.imwrite(os.path.join(output_dir, relative_path), image_res)
    except Exception as error:
        print(error)

    #return image_res, label_coord

# Run on all figures
#for i in range(400):
#   figure_only(i)