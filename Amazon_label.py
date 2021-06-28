import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import json
import os
from scipy.spatial import distance
import glob

"""
This function takes the images path, amazon labels results, and optionally
the output directories (for images and json file)
"""

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help = "Figures input directory")
    parser.add_argument("--amazonDirectory", help = "Amazon label bounding boxes")
    parser.add_argument("--outputDirectory", help = "directory to save the segmented images")
    parser.add_argument("--jsonDirectory", help = "directory to save the json output")
    
    return parser


def get_amazon_labels():
    amazon_files = []
    parser = get_args()
    args = parser.parse_args()
    #img_paths = args.file_path
    amazon_paths = args.amazonDirectory
    amazon_dir = os.listdir(amazon_paths)
    for path in amazon_dir:
        file = os.path.join(amazon_paths, path)
        amazon_files.append(file)
    return amazon_files
    


"""This function receives each figure path and loads it"""
def extract_json_files(i):
    amazon_files = get_amazon_labels()
    # Extract the contents of the json files 
    with open(amazon_files[i], 'r', encoding="utf-8") as json_file:
        label_info = json.load(json_file)
        json_file.close()
    return label_info


"""This function takes in the label info and returns label
bounding box and label name
"""

def extract_label_bboxes(index):
    bounding_boxes = {}
    label_name = {}
    label_info = extract_json_files(index)
    try:
        
        if type(label_info) is dict and "TextDetections" in label_info.keys():
            contents = label_info['TextDetections']
            for i, j in enumerate(contents):
                if j['Type'] == 'LINE' and j["Confidence"] >= 75:
                    bbox = j['Geometry']['BoundingBox']
                    label = j['DetectedText']
                    bounding_boxes[i] = bbox
                    label_name[i] = label
        else:
            for i, j in enumerate(label_info):
                if j['Type'] == 'LINE' and j["Confidence"] >= 75:
                    bbox = j['Geometry']['BoundingBox']
                    label = j['DetectedText']
                    bounding_boxes[i] = bbox
                    label_name[i] = label
    except Exception as error:
        print(error)
    
    return bounding_boxes, label_name

    
