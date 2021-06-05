import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
from amazon_dist_calc import *
from Amazon_label import *

""""
This function takes in the index of the figure label, extracts the dimensions
of the label coordinates, and converts it back to the original unit.
We import label_info, extract_label_bboxes from Amazon_label
"""
def label_points(index):
    image, edged, h, w = image_processing(index)
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
