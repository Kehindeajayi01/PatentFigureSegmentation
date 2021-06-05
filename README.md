# PatentFigureSegmentation
This project involves segmenting figures and labels in patent figures. 
The following steps were carried out in order to perform the segmentation:

. We use Amazon Rekognition tool to obtain bounding box coordinates for the figure labels

. We use the coordinates obtained in step 1 to wipe off the figure labels

. Then, we use Contour detection method to detect the subfigures for images with subfigures.

. Finally, we use distance measure to associate the figure labels with their corresponding figures.

