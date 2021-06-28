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


def finetune_label(label_name):
    prefixes = ("FIG", "figure", "Figure", "fig", "FIGURE", "Fig")
    prefixes2 = ("FIG.", "figure.", "Figure.", "fig.", "FIGURE.", "Fig.")
    suffix = "."
    new_label_name = {}
    try:
        
        if len(label_name) == 1:
            for k, v in label_name.items():
                new_label_name[k] = v
        else:
        
            keys = list(label_name.keys())
            val = list(label_name.values())
            left = 0
            right = 1
            while right < len(keys) and left < len(keys):
                # First value starts with "FIG" and ends with a number
                if (val[left].startswith(prefixes) or val[left].startswith(prefixes2)) and val[left].endswith(tuple("0123456789")):
                    new_label_name[keys[left]] = val[left]
                    left += 1
                # Second starts with a "FIG" and ends with a number
                elif (val[right].startswith(prefixes)or val[right].startswith(prefixes2)) and val[right].endswith(tuple("0123456789")):
                    new_label_name[keys[right]] = val[right]
                    right += 1
                # first starts with a number and second starts with a "FIG" and ends with a number
                elif val[left].startswith(tuple("0123456789")) and val[right].startswith(prefixes) and val[right].endswith(suffix):
                    name = val[right] + val[left]
                    new_label_name[keys[left]] = name
                    left += 1
                    right += 1
                # first starts with a number and second starts with a "FIG"
                elif val[left].startswith(tuple("0123456789")) and val[right].startswith(prefixes):
                    name = val[right] + " " + val[left]
                    new_label_name[keys[left]] = name
                    left += 1
                    right += 1
                # first and second start with a number
                elif val[left].startswith(tuple("0123456789")) and val[right].startswith(tuple("0123456789")):
                    right += 1
                # first starts with a "FIG" and second starts with a number
                elif val[left].startswith(prefixes) and val[right].startswith(tuple("0123456789")):
                    left += 1
                    right += 1
                
                else:
                    right += 1
    except Exception as error:
        print(error)
    return new_label_name
            

# function to generate our json file
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
    new_label_name = finetune_label(label_name)
    # case for figure with subfigures
    json_name['patent_id'] = relative_path[:19]
    json_name["Figure_file"] = relative_path
    json_name["n_subfigures"] = len(new_label_name)
    crop_image(index)
    for key, val in new_label_name.items():
        sub_file = {}
        num = ""
        for c in val:
            if c.isdigit():
                num += c
            
        sub_file["subfigure_id"] = int(num) if num.isdigit() else (num + ".")
        sub_file["subfigure_file"] = (relative_path + "_" + num) if num.isdigit() else (relative_path + "_" + ".")
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
            #print(f"Image {i} is successfully segmented")
        fp.close()
        print("Done!")
    
    return f"Total segmented images: {len(rel_paths)}"

results = output_json()
print(results)



        