import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
from Amazon_label import *
import argparse

#we obtained get_args() from Amazon_label

"""This function collects all the figure files"""
def get_files():
    files = []
    parser = get_args()
    args = parser.parse_args()
    img_dir = args.file_path
    rel_paths = os.listdir(img_dir)
    for path in rel_paths:
        file = os.path.join(img_dir, path)
        files.append(file)
    return files

#img_paths = get_files()

# function to get the height and width of the image
def get_width_height(index):
    img_paths = get_files()
    img_path = img_paths[index]
    img = cv2.imread(img_path)
    image_res = cv2.resize(img, None, fx = 0.3, fy = 0.3, interpolation=cv2.INTER_AREA)
    h, w = image_res.shape[:2]
    return h, w
""""
This function takes in the index of the figure label, extracts the dimensions
of the label coordinates, and converts it back to the original unit.
We import label_info, extract_label_bboxes from Amazon_label
"""
def label_points(index):
    h, w = get_width_height(index)
    bbox, _ = extract_label_bboxes(index)
    label_conv_points = []
    for k, v in bbox.items():
        width, height = v['Width'], v['Height']
        left, top = v['Left'], v['Top']
    
        # convert back the amazon coordinates to the original coordinates
        width = int(width * w)
        height = int(height * h)
        left = int(left * w)
        top = int(top * h)
        label_conv_points.append((left, width, top, height))
    # return the label_cent list
    return label_conv_points
