from amazon_dist_calc import *
from segmentation_pipeline import label_points
import cv2
import numpy as np          

# This function loads the image and wipe out the labels 
# using label coordinates from Amazon Rekognition tool
def figure_only(index):

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
        image_res[top : top + height, left: left + width] = (255, 255, 255)
        label_coord = label_coord[0]
    else:  
        # case for image with subfigures
        for label in label_coord:
            # unpack the coordinates
            left, width, top, height = label
            # set the pixels in those location to zero
            image_res[top : top + height, left: left + width] = (255, 255, 255)

    return image_res, label_coord

# This function accepts the figure only and detect the edges in the figures
def detect_edge(index):
    image_res, label_coord = figure_only(index)
    # convert to a grayscale image, and apply thresholding
    gray = cv2.cvtColor(image_res, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the image to remove some noise
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # Use Canny edge detector to detect the edges
    edged = cv2.Canny(blurred, 50, 200)
    # dilate and erode the image to close any gaps in the edge detected
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    return image_res, edged, gray

# This function draw contours around the edge detected
def draw_contour(index):
    image_res, edged, gray = detect_edge(index)
    image_coord = []
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop through the contours
    for c in cnts:
        if cv2.contourArea(c) > 1000:
            # find the minimum area   
            rect = cv2.minAreaRect(c)
            # calculate the coordinates of the minimum area rectangle
            box = cv2.boxPoints(rect)
            # Convert the coordinates to integers
            box = np.int0(box)
            image_coord.append(np.abs(box))
        
    #        cv2.drawContours(image_res, [box], 0, (0, 255, 0), 2)
    #        cv2.imshow("Image only", image_res)
    #        cv2.imwrite("img_ex11.jpg", image_res)
    #        cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image_coord 

