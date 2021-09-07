# PatentFigureSegmentation
This project involves segmenting figures and labels in patent figures using Contour method. 
The following steps were carried out in order to perform the segmentation:

- We use Amazon Rekognition tool to obtain bounding box coordinates for the figure labels

- We use the coordinates obtained in step 1 to wipe off the figure labels

- Then, we use Contour detection method to detect the subfigures for images with subfigures.

- Finally, we use distance measure to associate the figure labels with their corresponding figures.


## Note
- This pipeline assumes you have the directory for all the figures and also the directory for the labels obtained from Amazon 
Rekognition tool.

- So, to segment all your figures and generate a json file which contains the patent id, figure file and figure label, 
- run python image_to_json.py path/to/images -- amazonDirectory path/to/amazon_labels --outputDirectory output/path --jsonDirectory path/to/store/json 
- Output will be segmented figures and a json file that consists of image_id, labels, etc. will be saved.
