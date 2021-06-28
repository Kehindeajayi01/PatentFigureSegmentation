import numpy as np           
import cv2
from amazon_test import *
from Amazon_label import get_args
import os
import pathlib
from segmentation_pipeline import label_points, get_files

def crop_image(index):
    _, gray = detect_edge(index)
    image_coord = draw_contour(index)
    parser = get_args()
    args = parser.parse_args()
    img_dir = args.file_path
    output_dir = args.outputDirectory
    rel_paths = os.listdir(img_dir)
    relative_path = rel_paths[index]
    # Added code
    #img_paths = get_files()
    #img_path = img_paths[index]  # img_path to read the image
    
    
    #End code
    # function to return the file extension
    file_extension = pathlib.Path(relative_path).suffix
    
    try:
        
        if len(image_coord) == 1:
            # resize the image
            #image = cv2.imread(img_path)
            #image_res = cv2.resize(image, None, fx = 0.3, fy = 0.3, interpolation=cv2.INTER_AREA)
            #label_coord = label_points(index)
            #left, width, top, height = label_coord[0]
            # set the pixels in those location to zero
            #image_res[(top) : (top + height), (left): (left + width)] = (255, 255, 255)
            #cv2.imwrite(os.path.join(output_dir, relative_path), image_res)
            x = np.abs(min(image_coord[0][0][0], image_coord[0][1][0], image_coord[0][2][0], image_coord[0][3][0]))
            w =  np.abs(max(image_coord[0][0][0], image_coord[0][1][0], image_coord[0][2][0], image_coord[0][3][0]))
            y =  np.abs(min(image_coord[0][0][1], image_coord[0][1][1], image_coord[0][2][1], image_coord[0][3][1]))
            h =  np.abs(max(image_coord[0][0][1], image_coord[0][1][1], image_coord[0][2][1], image_coord[0][3][1]))
            seg_image = gray[y : h, x : w]
            cv2.imwrite(os.path.join(output_dir, relative_path), seg_image)
        else:  
            for i, coord in enumerate(reversed(image_coord)):
                x = np.abs(min(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                w = np.abs(max(coord[0][0], coord[1][0], coord[2][0], coord[3][0]))
                y = np.abs(min(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                h = np.abs(max(coord[0][1], coord[1][1], coord[2][1], coord[3][1]))
                seg_image = gray[y : h, x : w]
                cv2.imwrite(os.path.join(output_dir, relative_path + "_" + str(i) + file_extension), seg_image)
    except Exception as error:
        print(f"Image with error: {relative_path}")
        print(error)
       
        