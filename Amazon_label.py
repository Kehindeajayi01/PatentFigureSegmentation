import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
import glob

"""
This function takes in Amazon rekognition result and extract the 
bounding box coordinates.
"""
path_to_json = 'C:/Users/ajayi/OneDrive/Desktop/Research/awsrek100patents/*.json'

"""
This function gets the entire Amazon results file paths
"""
def get_files(file_path):
    files = glob.glob(file_path)
    return files

json_files = get_files(path_to_json)


"""This function receives each figure path and loads it"""
def extract_json_files(file, i):
    # Extract the contents of the json files 
    with open(file[i], 'r') as json_file:
        label_info = json.load(json_file)
        json_file.close()
    return label_info


"""This function takes in the label info and returns label
bounding box and label name
"""
def extract_label_bboxes(index):
    bounding_box = {}
    label_name = {}
    label_info = extract_json_files(json_files, index)  # json_files consists of the entire 100 figures
    contents = label_info['TextDetections']
    for i, j in enumerate(contents):
        if j['Type'] == 'LINE':
            bbox = j['Geometry']['BoundingBox']
            label = j['DetectedText']
            bounding_box[i] = bbox
            label_name[i] = label
    
    return bounding_box, label_name


    
