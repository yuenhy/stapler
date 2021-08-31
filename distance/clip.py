import torch
import torch.nn.functional as F
import torch.nn as nn
import clip
from PIL import Image
from tqdm import tqdm
import h5py
import clip
import time
import numpy as np
from pathlib import Path

def measure_distance(original, generated):
  # distance = 0
  return F.mse_loss(original, generated)

# https://github.com/openai/CLIP/blob/main/clip/model.py#L354
# https://github.com/openai/CLIP/blob/main/clip/model.py#L291
def calculate_logits(image_features, text_features):
  logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))

  # normalize
  image_features = image_features / image_features.norm(dim=-1, keepdim=True)
  text_features = text_features / text_features.norm(dim=-1, keepdim=True)

  # cosine similarity as logits
  logit_scale = logit_scale.exp()
  logits_per_image = logit_scale * image_features @ text_features.t()
  logits_per_text = logit_scale * text_features @ image_features.t()

  # shape = [global_batch_size, global_batch_size]
  return logits_per_image, logits_per_text

def calculate_prob(image_features, text_features):
  logits_per_image, logits_per_text = calculate_logits(image_features, text_features)
  probs = logits_per_image.softmax(dim=-1).cpu().numpy()
  return probs

# encodes image, encodes text
def generate_clip_score(device, img, text):
  model, preprocess = clip.load("ViT-B/32", device=device)
  image = preprocess(Image.open(img)).unsqueeze(0).to(device)
  with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    probs = calculate_prob(image_features, text_features)
  return probs

def get_image_encoding(img, folder="encoding"):
  device = "cuda" if torch.cuda.is_available() else "cpu"
  output_folder = Path(folder)
  output_folder.mkdir(parents=True, exist_ok=True)
  model, preprocess = clip.load("ViT-B/32", device=device)
  image = preprocess(Image.open(img)).unsqueeze(0).to(device)
  filename = Path(img).stem
  filepath = output_folder.joinpath(f"{filename}.hdf5")
  with torch.no_grad():
    image_features = model.encode_image(image)
  with h5py.File(str(filepath), "w") as f:
    f.create_dataset("encoding", data=image_features.cpu())

# load image features from file, encode text
def get_clip_score(device, encoded_img, text):
  model, _ = clip.load("ViT-B/32", device=device)
  
  with h5py.File(str(encoded_img), 'r') as hf:
    image_features = hf["encoding"][:]

  with torch.no_grad():
    text_features = model.encode_text(text)
    probs = calculate_prob(image_features, text_features)
  
  return probs
    

def score_by_clip(original_imgs, generated_imgs, prompts, original_encodings=False):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    probs = []

    for i in tqdm(range(len(generated_imgs))):

        model, preprocess = clip.load("ViT-B/32", device=device)
        text = clip.tokenize(prompts[i]).to(device)
        prob = 0

        if original_encodings: # existing encodings
          prob = get_clip_score(device, original_encodings[i], text).tolist()[0]
        else: # no existing encoding, get fresh encoding
          prob = generate_clip_score(device, generated_imgs[i], text).tolist()[0]

        probs.append(prob)

    return probs