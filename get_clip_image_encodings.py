import torch
import clip
from PIL import Image
from pathlib import Path
import h5py
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

input_folder = Path("wga")
output_folder = Path("wga_encoding")
replace = False

folder = list(input_folder.glob("*.jpg"))


for i in tqdm(range(len(folder))):
    img = folder[i]
    filename = img.stem
    filepath = output_folder.joinpath(f"{img.stem}.hdf5")

    if filepath.exists() and not replace:
        pass

    image = preprocess(Image.open(img)).unsqueeze(0).to(device)

    with torch.no_grad():
        image_features = model.encode_image(image)
        text = clip.tokenize(["a painting"]).to(device)
        logits_per_image, logits_per_text = model(image, text)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()

    print("Label probs:", probs)


    with h5py.File(str(filepath), "w") as f:
        f.create_dataset("encoding", data=image_features)


# folder = list(output_folder.glob("*.hdf5"))
# print(folder)

# for i in tqdm(range(len(folder))):
#     filepath = folder[i]
#     with h5py.File(str(filepath), 'r') as hf:
#         image_features = hf["encoding"][:]

#     with torch.no_grad():
#         text = clip.tokenize(["a painting"]).to(device)
#         logits_per_image, logits_per_text = model(image, text)
#         probs = logits_per_image.softmax(dim=-1).cpu().numpy()
    
#     print("Label probs:", probs)



    
    
