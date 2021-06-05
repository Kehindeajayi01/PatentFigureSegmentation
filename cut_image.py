import numpy as np           
import cv2
from segment_image import draw_contour, detect_edge
from amazon_dist_calc import *
import os

def crop_image(index):
    cleaned_image, edged, gray = detect_edge(index)
    image_coord = draw_contour(index)
    start = "C:/Users/ajayi/OneDrive/Desktop/100patents_design_jpg/patent_images"
    relative_path = os.path.relpath(img_paths[index], start)
    
    try:
        
        if len(image_coord) == 1:
            x = np.abs(min(image_coord[0][1][0], image_coord[0][3][0]))
            w =  np.abs(max(image_coord[0][1][0], image_coord[0][3][0]))
            y =  np.abs(min(image_coord[0][1][1], image_coord[0][3][1]))
            h =  np.abs(max(image_coord[0][1][1], image_coord[0][3][1]))
            seg_image = gray[y : y + h, x : x + w]
            cv2.imwrite(relative_path, seg_image)
        else:  
            for i, coord in enumerate(reversed(image_coord)):
                x = np.abs(min(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                w = np.abs(max(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                y = np.abs(min(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                h = np.abs(max(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                seg_image = gray[y : y + h, x : x + w]
                cv2.imwrite(relative_path + "_" + str(i) + ".jpg", seg_image)
    except Exception as error:
        print(f"Image with error: {relative_path}")
        print(error)
       
        
#crop_image(1)