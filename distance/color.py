from platform import dist
import numpy as np
from tqdm import tqdm
from skimage.color import rgb2hsv
from skimage.io import imread
import scipy.spatial.distance as ssd
# import matplotlib.pyplot as plt


def get_hue_img(img_path):
    img = imread(img_path)
    hsv_img = rgb2hsv(img)
    hue_img = hsv_img[:,:,0]
    return hue_img

def get_hist(img, bins=50):
    hist = np.histogram(img.flatten(), bins)
    # plt.hist(hist, bins='auto') 
    # plt.show()
    return hist

def measure_hist_distance(original_hist, generated_hist, method):
    dist = 0
    if method == "correlation":
        # 0 perfect correlation
        # 1 no correlation
        # 2 perfect inverse correlation
        dist = ssd.correlation(original_hist, generated_hist)
    elif method == "chebyshev":
        dist = ssd.chebyshev(original_hist, generated_hist)
    elif method == "euclidean":
        dist = ssd.euclidean(original_hist, generated_hist)
    return dist

def score_by_color(original_imgs, generated_imgs, method="correlation"):
    distances = []
    for i in tqdm(range(len(generated_imgs))):
        generated_hue_img = get_hue_img(generated_imgs[i])
        original_hue_img = get_hue_img(original_imgs[i])

        generated_hist, _ = get_hist(generated_hue_img)
        original_hist, _ = get_hist(original_hue_img)

        distance = measure_hist_distance(original_hist, generated_hist, method)
        distances.append(distance)
    return distances