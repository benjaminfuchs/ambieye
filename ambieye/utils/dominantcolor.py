""" from https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/ """

from collections import Counter
from sklearn.cluster import KMeans
import cv2
import numpy as np

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input and returns the dominant color as an rgb array
    
    dominant color is found by performing k means on the pixel colors and returning the centroid
    of the largest cluster

    processing time is sped up by working with a smaller image; this can be done with the 
    image_processing_size param which takes a tuple of image dims as input
    """
    # read in image of interest
    bgr_image = cv2.imread(image)
    # convert to HSV; this is a better representation of how we see color
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    # extract dominant color 

    # resize image if new dims provided
    if image_processing_size is not None:
        hsv_image = cv2.resize(hsv_image, image_processing_size, interpolation = cv2.INTER_AREA)
    
    # reshape the image to be a list of pixels
    hsv_image = hsv_image.reshape((hsv_image.shape[0] * hsv_image.shape[1], 3))

    # cluster the pixels and assign labels
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(hsv_image)

    # count labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    # create 1px rgb image from color
    dominant_color = np.uint8([[dominant_color]]) 
    rgb_image = cv2.cvtColor(dominant_color, cv2.COLOR_HSV2RGB)

    return rgb_image.tolist()[0][0]
