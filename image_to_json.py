import numpy as np           
import cv2
import glob
from Amazon_label import extract_label_bboxes
from amazon_test import *
import os
import string
from random import choice
import json
from cut_image import crop_image
from segmentation_pipeline import get_args


def format_label(label_name):
    prefixes = ("FIG", "figure", "Figure", "fig", "FIGURE", "Fig")
    suffix = "."
    new_label_name = {}
    try:
        
        if len(label_name) > 1:
        
            for k, v in label_name.items():
                if v.startswith(prefixes) and v.endswith(tuple("0123456789")):
                    new_label_name[k] = v
    
                elif v.startswith(tuple("0123456789")) and label_name[k + 1].startswith(prefixes) and \
                    label_name[k+ 1].endswith(suffix):
                    name = label_name[k + 1] + v
                    new_label_name[k] = name
                
        elif len(label_name) == 1:
            for k, v in label_name.items():
                new_label_name[k] = v
    except Exception as error:
        print(error)
    return new_label_name

# function to generate our json file
def patent_json(index):
    chars = string.digits
    json_name = {}
    sub_list = []

    # get patent id
    parser = get_args()
    args = parser.parse_args()
    img_paths = args.file_path
    rel_paths = os.listdir(img_paths)
    relative_path = rel_paths[index]
    _, label_name = extract_label_bboxes(index)

    # call the function to format the label_name
    new_label_name = format_label(label_name)
    # case for figure with subfigures
    json_name['patent_id'] = relative_path
    json_name["fig_id"] =  ''.join(choice(chars) for _ in range(4))
    json_name["n_subfigures"] = len(new_label_name)
    crop_image(index)
    for key, val in new_label_name.items():
        sub_file = {}
        sub_file['subfigure_id'] = key + 1
        sub_file['subfigure_file'] = relative_path + "_" + str(key) + ".jpg"
        sub_file["subfigure_label"] = val
        sub_list.append(sub_file)
        
    json_name['subfigurefile'] = sub_list
    
    return json_name

def output_json():
    parser = get_args()
    args = parser.parse_args()
    json_output = args.jsonDirectory
    img_paths = args.file_path
    rel_paths = os.listdir(img_paths)
    with open(os.path.join(json_output, 'test.json'), 'w', encoding='utf-8') as fp:
        for i in range(len(rel_paths)):
            sample = patent_json(i)
            json.dump(sample, fp, ensure_ascii=False)
            fp.write("\n")
            print(f"Image {i} is successfully segmented")
        fp.close()
        print("Done!")
    
    return f"Total segmented images: {len(rel_paths)}"

results = output_json()
print(results)



        