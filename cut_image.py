import numpy as np           
import cv2
from amazon_test import *
from segmentation_pipeline import get_args
import os

def crop_image(index):
    _, gray = detect_edge(index)
    image_coord = draw_contour(index)
    parser = get_args()
    args = parser.parse_args()
    img_paths = args.file_path
    output_dir = args.outputDirectory
    rel_paths = os.listdir(img_paths)
    relative_path = rel_paths[index]
    
    try:
        
        if len(image_coord) == 1:
            x = np.abs(min(image_coord[0][1][0], image_coord[0][3][0]))
            w =  np.abs(max(image_coord[0][1][0], image_coord[0][3][0]))
            y =  np.abs(min(image_coord[0][1][1], image_coord[0][3][1]))
            h =  np.abs(max(image_coord[0][1][1], image_coord[0][3][1]))
            seg_image = gray[y : y + h, x : x + w]
            cv2.imwrite(os.path.join(output_dir, relative_path), seg_image)
        else:  
            for i, coord in enumerate(reversed(image_coord)):
                x = np.abs(min(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                w = np.abs(max(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                y = np.abs(min(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                h = np.abs(max(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                seg_image = gray[y : y + h, x : x + w]
                cv2.imwrite(os.path.join(output_dir, relative_path + "_" + str(i) + ".jpg"), seg_image)
    except Exception as error:
        print(f"Image with error: {relative_path}")
        print(error)
       
        