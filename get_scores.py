from pathlib import Path
from distance import score_by_style, score_by_content, score_by_color
import extra

original_imgs = []
generated_imgs = []

folder = Path("datasets/art")
for i in folder.glob("*.png"):
    original_name = i.name.split("_")
    original_name = f"{'_'.join(original_name[:-1])}.jpg"
    original_img = folder.joinpath(original_name) 
    if original_img.exists():
        generated_imgs.append(str(i))
        original_imgs.append(str(original_img))

generated_imgs = generated_imgs[:50]
original_imgs = original_imgs[:50]

distances = score_by_content(original_imgs=original_imgs, generated_imgs=generated_imgs)
df = extra.convert_to_df(original_imgs=original_imgs, generated_imgs=generated_imgs, distances=distances)
df.to_csv("50_artworks_scored_by_content.csv", index=False)
# extra.display_results(df)


