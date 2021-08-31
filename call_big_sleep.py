from big_sleep.big_sleep import exists
import fire
import random as rnd
from big_sleep import Imagine, version
from pathlib import Path
import pandas as pd
import shutil
import sys
import json

from torch.optim import adam

print(f'calling big sleep with prompts')

save_dir = "images from prompts"
prompt_list = "prompt_reference_list.csv"
output_session_settings = True

if len(sys.argv) == 2:
    save_dir = sys.argv[1]
elif len(sys.argv) == 3:
    save_dir = sys.argv[1]
    prompt_list = sys.argv[2]

settings_file = Path(save_dir).joinpath("settings.json")
Path(save_dir).mkdir(exist_ok=True, parents=True)

# df = pd.read_csv(prompt_list, header=None)
df = pd.read_csv(prompt_list)
new_list_path = Path(save_dir).joinpath(prompt_list)
shutil.move(prompt_list, new_list_path)

for row in df.itertuples():
    # columns=["REF_ID", "PROMPT", "PROMPT_FORMAT", "START_LATENT", "GENERATED_IMG", "REFERENCE_IMG"])
    latents_filename = None
    new_latents_path = Path(save_dir).joinpath(f"latents/{row.START_LATENT}")
    if new_latents_path.exists():
        latents_filename = row.START_LATENT
    prompt = " ".join(row.PROMPT)
    imagine = Imagine(
        text=prompt,
        img=None,
        text_min="",
        lr = 5e-2,
        image_size = 512,
        gradient_accumulate_every = 1,
        epochs = 1,
        iterations = 1050,
        save_every = 1000,
        save_progress = False,
        save_date_time = False,
        save_dir = save_dir,
        bilinear = False,
        open_folder = False,
        seed = 0,
        append_seed = False,
        torch_deterministic = False,
        max_classes = None,
        class_temperature = 2.,
        save_best = False,
        experimental_resample = False,
        ema_decay = 0.5,
        num_cutouts = 32,
        center_bias = False,
        save_latents = "initial",
        latents_filename = latents_filename
    )

    if output_session_settings:
        output_session_settings = False
        settings = imagine.__dict__.copy()
        keys = imagine.__dict__.copy().keys()

        for k in keys:
            if k.startswith("_"):
                settings.pop(k)
            else:
                settings[k] = str(settings[k])
            
        with open(settings_file, "w+") as f:
            json.dump(settings, f, indent=4)
    
    imagine()
    
    new_img_path = imagine.img_dir.joinpath(row.GENERATED_IMG)
    shutil.move(imagine.filename, new_img_path)
    
    if latents_filename is None:
        shutil.move(imagine.latents_filepath, new_latents_path)


