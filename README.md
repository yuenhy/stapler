# big sleep
Default Directory
```
./
├── images
│   └── *.png
├── latents
│   └── *.backup
├── settings.json
└── prompt_reference_list.csv
```
[Change Directory](https://github.com/yuenhy/big-sleep#usage)

You can change the parent directory with

```bash
$ dream "the edge of human" --save_dir secret_experiment
```

[Change subdirectory](https://github.com/yuenhy/big-sleep/blob/main/big_sleep/big_sleep.py#L344) (inline code)

[Saving and Restoring Latents](https://github.com/yuenhy/big-sleep#saving-and-restoring-latents)

Saves `initial`izing latent or as per `save_every`. Defaults to False

```bash
$ dream 'androids dreaming of electric sleep' --save_latents initial|True
```

Restores latents and resets optimizer.

```bash
$ dream 'a latent space' --latents_filename latent.pkl
```
Looks for `latent.pkl` in `latents` wherever the command is invoked.
You can specify the parent directory with `--save_dir`.


No tqdm output
```
from tqdm import tqdm
from functools import partialmethod
tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
```
# colab
some examples [here](https://colab.research.google.com/drive/1S4z9yKZjL1OYPfJlYdLKP5c5xb6t2M0u)
slurm script [here](https://gist.github.com/yuenhy/068ac13ae872b76d7d15b6bbde96c082)

# distance functions
measure distance between the original image and the generated image

## score_by_color(original_imgs, generated_imgs, method="correlation")

* **original_imgs**: list that contains filepaths to images 
* **generated_imgs**: list that contains filepaths to images 
* **method**: correlation|chebyshev|euclidean

uses methods from [`scipy.spatial.distance`](https://docs.scipy.org/doc/scipy/reference/spatial.distance.html) to [compare between hue histograms](https://github.com/yuenhy/stapler/blob/main/distance/color.py#L22)

returns list of distances

make changes in `distance/color.py`

## score_by_style(original_imgs, generated_imgs)

* **original_imgs**: list that contains filepaths to images 
* **generated_imgs**: list that contains filepaths to images 

uses normalized gram matrix of `style_layers = block1_conv1, block2_conv1, block3_conv1, block4_conv1, block5_conv1`, with distance calculated by `torch.nn.functional.mse_loss`

returns list of distances

change layers in `distance/vgg.py`,
change distance function in `distance/neural_style.py`

## score_by_content(original_imgs, generated_imgs)

* **original_imgs**: list that contains filepaths to images 
* **generated_imgs**: list that contains filepaths to images 
  
gets `content_layers = block4_conv2`, with distance calculated by `torch.nn.functional.mse_loss`

returns list of distances

change layers in `distance/vgg.py`,
change distance function in `distance/neural_style.py`

## score_by_clip(original_imgs, generated_imgs, prompts, original_encodings)

* **original_imgs**: list that contains filepaths to images 
* **generated_imgs**: list that contains filepaths to images 
* **prompts**: list of lists of prompt parts (see example) to encode
* **original_encodings**: list that contains filepaths to CLIP latents, use `False` if does not exists
  
currently returns the probabilities of prompt parts on original_imgs

### image encodings
original_encoding should be a [`.hdf5`](https://docs.h5py.org/en/stable/quick.html#appendix-creating-a-file) containing the `encoding` dataset which `data=image_features`

to use within a loop:
* get_image_encoding(img) in `distance/clip.py` to save image features in a `.hdf5` file
* get_clip_score(encoded_img, text) in `distance/clip.py` to use image features

# prompt generator

## grammar.py
declare valid grammar, custom flag, custom fill method here

### grammar
* nofix - nf - `no_extra` formatting
* prefix - pf - prepend word(s)
* suffix - sf - append word(s)
* afix - af - prepend & append, e.g. parenthesis

if you end up using custom strings, you might want `no_extra` words/ formatting, so you would want to specify `_nf`.

change word formatting in formats.py

### custom flag
default `custom_flag = cusz`

change flag in grammar.py

### horizontal fill
if horizontal fill, `change_axis = False`
```
cusz_0 = ["foo", "baz"]
if prompt_format = "cusz_0-bar-cusz_0"
then prompt = ["foo", "bar", "baz"]
```
change axis in grammar.py

### vertical fill
if vertical fill, `change_axis = True`
```
cusz_colors = ["red", "blue"]
cusz_animal = ["zebra", "horse"]
if prompt_format = "cusz_colors-cusz_animal"
then prompt = ["red", "horse"]
```
change axis in grammar.py

## custom_strings.py
declare custom strings here
```
<custom_flag>_listOfStrings = ["foo", "bar"]
```

## formats.py
unfortunately not a class 

* nofix - nf - `no_extra` formatting
* prefix - pf - prepend word(s)
* suffix - sf - append word(s)
* afix - af - prepend & append, e.g. parenthesis

```
def get_author_format(fix, data):
    prefix = ["in_style_of", "by"]
    nofix = ["no_extra"]
    types = ["lname", "fullname"]

    ...

if prompt_format = ["author_pf"]
then prompt = ["in_style_of_author]

to change how valid_grammar is being used -> get_prompt_format()
call to function is in generator.py -> get_prompt_ref_list()

```

## generator.py
**caution designed specifically for wga's catalogue.csv**
parser here

### prompt_reference_list.csv
REF_ID prompts/generator.py -> make_prompts()
PROMPT prompts/generator.py -> parse_format()
PROMPT_FORMAT prompts/generator.py -> parse_format()
START_LATENT prompts/generator.py -> get_prompt_reference_list()
GENERATED_IMG `prompts/generator.py` -> get_prompt_reference_list()
REFERENCE_IMG `prompts/generator.py` -> get_prompt_reference_list()

### make_prompts(csv, filename=None, aw=50, pp=5, runs=5)
for `aw` artworks, make `pp` prompts; each prompt will run `runs` times\
for 50 artworks, make 5 prompts; each prompt will run 5 times 

### parse_format(row, prompt_format)
change `data` [dict](https://github.com/yuenhy/stapler/blob/main/prompts/generator.py#L11) as per  input data

#### manually specify artist to sample from
```
custom = {
    "italian": ["RAFFAELLO Sanzio", "MICHELANGELO Buonarroti"],
    "french": ["INGRES, Jean-Auguste-Dominique", "DELACROIX, Eugène"]
}

if aw = "italian" and max_pieces = 10
then sample at most 10 artworks from RAFFAELLO Sanzio and MICHELANGELO Buonarroti
```

# artist_*.csv
## artist_mid.csv
instead of [`q=raphael`](https://trends.google.com/trends/explore?date=2004-01-01%202021-08-28&q=raphael), specify [`q=/m/0c43g`](https://trends.google.com/trends/explore?date=2004-01-01%202021-08-28&q=%2Fm%2F0c43g) to get italian painter instead of a certain tmnt


[pytrends](https://github.com/GeneralMills/pytrends) unoffical api for google trends

**caution you hit rate limits too easily**
https://github.com/GeneralMills/pytrends#caveats

**mid not checked** but you can
look at `artist_web_searches.csv` and `artist_images.csv if gprop=images`




## artist_ngram_values.csv
to note:\
290,William Blake,1.2983765081404324e-05,william-blake \
291,William Hogarth,1.877850906458435e-06,william-hogarth\
292,William Merritt Chase,3.4047360178324484e-05,william-merritt-chase\
293,William Turner,3.4047360178324484e-05,william-merritt-chase\
294,William-Adolphe Bouguereau,5.6879872040769384e-05,william-adolphe-bouguereau\

78,Francisco Goya,3.6826480416291795e-07,francisco-goya\
79,Francisco de Zurbaran,2.187341925721274e-06,francisco-de-zurbaran\

116,Henri Fantin-Latour,6.9500538471472556e-06,henri-fantin-latour\
117,Henri Martin,2.4208597507560395e-06,henri-martin\
118,Henri Matisse,1.3240138855773038e-06,henri-matisse\
119,Henri Rousseau,9.298228086131178e-08,henri-rousseau\
120,Henri de Toulouse-Lautrec,3.7809406990356357e-07,henri-de-toulouse-lautrec\
121,Henri-Edmond Cross,5.426108356080219e-06,henri-edmond-cross\

235,Pierre Bonnard,3.958794223744976e-07,pierre-bonnard\
236,Pierre Puvis de Chavannes,1.2302851597756347e-07,pierre-puvis-de-chavannes\
237,Pierre-Auguste Renoir,1.8887064068530248e-06,pierre-auguste-renoir\
238,Pierre-Paul Prud'hon,5.879820923614441e-07,pierre-paul-prud-hon\

# requirements.txt
probably has more than required\
[pip-check-reqs](https://github.com/r1chardj0n3s/pip-check-reqs) might help
```
$ git clone https://github.com/yuenhy/stapler.git
$ cd stapler
$ python -m clip-venv
$ pip install -r requirements.txt
$ pip install git+https://github.com/openai/CLIP.git
$ git clone https://github.com/yuenhy/big-sleep
$ cd big-sleep && pip install .
```