'''
- Removed the check if we have the mask_rcnn_coco.h5, put it as a comment at the bottom in case you want to add it back.
* Made it read it as an image instead of a vid
* Made the model load outside
* Made the old function take a model in param
+ Added a new function (same name so no prob) that calls the old one and gives it the model

##: Not sure what to do now but it feels like something is missing

'''


import os
import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
import time
from mrcnn.model import MaskRCNN
from pathlib import Path



# Configuration that will be used by the Mask-RCNN library
class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 1 + 80  # COCO dataset has 80 classes + one background class
    DETECTION_MIN_CßONFIDENCE = 0.6

ROOT_DIR = Path(".")

MODEL_DIR = os.path.join(ROOT_DIR, "logs")


COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# CHECK FOR RCNN HERE

# Create a Mask-RCNN model in inference mode
model = MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=MaskRCNNConfig())

# Load pre-trained model
model.load_weights(COCO_MODEL_PATH, by_name=True)
    

# Filter a list of Mask R-CNN detection results to get only the detected cars / trucks
def get_car_boxes(boxes, class_ids):
    car_boxes = []

    for i, box in enumerate(boxes):
        # If the detected object isn't a car / truck, skip it
        if class_ids[i] in [3, 8, 6]:
            car_boxes.append(box)

    return np.array(car_boxes)

def imagerec(p):
    return __imagerec(p, model)

def __imagerec(p, m):
    parked_car_boxes = None

    # Load the video file we want to run detection on
    image = cv2.imread(p)

    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_image = image[:, :, ::-1]

    # Run the image through the Mask R-CNN model to get results.
    results = m.detect([rgb_image], verbose=0)

    # Mask R-CNN assumes we are running detection on multiple images.
    # We only passed in one image to detect, so only grab the first result.
    r = results[0]

    # The r variable will now have the results of detection:
    # - r['rois'] are the bounding box of each detected object
    # - r['class_ids'] are the class id (type) of each detected object
    # - r['scores'] are the confidence scores for each detection
    # - r['masks'] are the object masks for each detected object (which gives you the object outline)

    # Filter the results to only grab the car / truck bounding boxes
    car_boxes = get_car_boxes(r['rois'], r['class_ids'])
   
    return len(car_boxes)


'''
if not os.path.exists(COCO_MODEL_PATH):
        mrcnn.utils.download_trained_weights(COCO_MODEL_PATH)
'''