""" from https://adamspannbauer.github.io/2018/03/02/app-icon-dominant-colors/ """

from collections import Counter
import logging
from sklearn.cluster import KMeans
import cv2
import numpy as np

LOGGER = logging.getLogger("root")

def get_dominant_color(bgr_image, brightness=0, k=4, image_processing_size = None):
    """
    takes an image as input and returns the dominant color as an rgb array
    
    dominant color is found by performing k means on the pixel colors and returning the centroid
    of the largest cluster

    processing time is sped up by working with a smaller image; this can be done with the 
    image_processing_size param which takes a tuple of image dims as input
    """
    # convert to HSV; this is a better representation of how we see color
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_image)

    lim = brightness
    v[v < lim] = 0
    v[v >= lim] -= brightness

    hsv_image = cv2.merge((h, s, v))

    # resize image if new dims provided
    if image_processing_size is not None:
        hsv_image = cv2.resize(hsv_image, (image_processing_size, image_processing_size), interpolation = cv2.INTER_AREA)

    # reshaping the image to be a list of pixels
    hsv_image = hsv_image.reshape((hsv_image.shape[0] * hsv_image.shape[1], 3))

    # clustering the pixels and assign labels
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(hsv_image)

    # counting labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    # create 1px rgb image from color
    dominant_color = np.uint8([[dominant_color]]) 
    rgb_image = cv2.cvtColor(dominant_color, cv2.COLOR_HSV2RGB)

    return rgb_image.tolist()[0][0]

def to_hex_color_string(color):
    return '#%02x%02x%02x' % (color[0], color[1], color[2])

def limit_diff(old_array, new_array, max_diff):
    for i, _ in enumerate(old_array):
        diff = old_array[i] - new_array[i]
        if diff > 0:
            old_array[i] = old_array[i] - min(abs(diff), max_diff)
        else:
            old_array[i] = old_array[i] + min(abs(diff), max_diff)

    return old_array

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)