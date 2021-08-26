from matplotlib.pyplot import figure, imshow
from matplotlib.image import imread
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def convert_to_df(original_imgs, generated_imgs, distances, method="correlation"):
    ascending = True
    descending = []
    if method in descending:
        ascending = False
    d = {
        "original_img": original_imgs,
        "generated_img": generated_imgs,
        "distance":distances
    }
    df = pd.DataFrame(data=d)
    df = df.sort_values(["original_img", "distance"], ascending=[True, ascending])
    return df

def display_results(df):
    name_original_imgs = df["original_img"].unique()
    # plt.clf()
    for i in name_original_imgs:
        filename = Path(i).name
        ordered_imgs = [i] + df[df.original_img == i]["generated_img"].tolist()
        ordered_distances = [filename] + df[df.original_img == i]["distance"].tolist()
        fig = figure(figsize=(20, 20))
        length = len(ordered_imgs)
        for k in range(length):
            # fig.tight_layout()
            a = fig.add_subplot(1, length, k+1)
            image = imread(ordered_imgs[k], 0)
            # image = plt.imread(ordered_imgs[k])
            plt.imshow(image, interpolation="nearest")
            if type(ordered_distances[k]) is str:
                plt.title(str(ordered_distances[k]))
            else:
                try:
                    plt.title(f"{ordered_distances[k]: .3f}")
                except Exception as e:
                    print(e)
                    plt.title(np.around(ordered_distances[k], 13))
            plt.axis("off")
        # plt.tight_layout()
        # plt.text(0, 0, f"variance = {np.var(ordered_distances[1:])}", ha="center", fontsize=18)
        plt.show()