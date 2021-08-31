#%%
import pandas as pd
from tqdm import tqdm
import time

from pytrends.request import TrendReq

from functools import partialmethod
tqdm.__init__ = partialmethod(tqdm.__init__, disable=False)

def save_trends(keycode, gprop, trends):
  df = pd.concat(trends, axis=1)
  df.columns = df.columns.droplevel(0) #drop outside header
  df = df.drop('isPartial', axis = 1) #drop "isPartial"
  df.reset_index(level=0,inplace=True) #reset_index
  names = []
  vs = list(keycode.values())
  ks = list(keycode.keys())
  for i in list(df.columns):
    if i in vs:
      j = vs.index(i)
      names.append(ks[j])
  df.columns= ["date"] + names #change column names
  df.to_csv(f"artist_{gprop}.csv", index=False, header=True)

import seaborn as sns
def visualize_trends(df):
  y = list(df.columns)[1:]
  sns.set(color_codes=True)
  dx = df.plot(figsize = (30,30),x="date", y=y, kind="line", title = "Interest Over Time")
  dx.set_xlabel('Date')
  dx.set_ylabel('Trends Index')
  dx.tick_params(axis='both', which='both', labelsize=10)

#%%
pytrends = TrendReq(hl='en-US', tz=360)
df = pd.read_csv("artist_ngram_values.csv")
artists = df.artist.to_list()

load_from_file = True
keycode = {}

if load_from_file:
  df = pd.read_csv("artist_mid.csv")
  for i, k in enumerate(df["artist"]):
    keycode[k] = (df["mid"])[i]
else:
  for j in tqdm(range(len(artists))):
    i = artists[j]
    sugg = pytrends.suggestions(keyword=i)
    if len(sugg) < 1:
      continue
    else:
      for j in sugg:
        types = ["painter", "impressionist", "artist", "illustrator", "sculptor", "poet"]
        for t in types:
          if t in j["type"].lower():
            keycode[i] = j["mid"]
            # stop iterating through types
            continue
    time.sleep(60)
ks = keycode.keys()
vs = keycode.values()
df_mid = pd.DataFrame([ks, vs], index=["artist", "mid"]).T
df_mid.to_csv("artist_mid.csv", index=False)

#%%
missing = []
for i in artists:
  if not i in keycode:
    missing.append(i)
print("missing:", missing)

#%%
trends = {}
success = []
gprop = "web_searches"

while not len(success) == len(keycode):
  exceptions = []
  for k, v in keycode.items():
    try:
        pytrends.build_payload(kw_list=[v], 
                            timeframe = 'all' # 2004 to present
                            ) 
        t = pytrends.interest_over_time()
        i += 1
        trends[i] = t
        success.append(k)
        time.sleep(60)
    except Exception as e:
        print(e)
        exceptions.append(k)
  if len(exceptions) > 0:
    print("retrying", len(exceptions))
print(f"got interest over time")
save_trends(keycode, gprop, trends)

#%%
df_web = pd.read_csv("artist_web_searches.csv")
visualize_trends(df_web.loc[:, :"Albrecht Dürer"])

#%%
trends = {}
success = []
gprop = "images"

while not len(success) == len(keycode):
  exceptions = []
  for k, v in keycode.items():
    try:
        pytrends.build_payload(kw_list=[v], 
                            timeframe = 'all', # queries 2004 to present, but results only appear from 2007
                            gprop = gprop
                            ) 
        t = pytrends.interest_over_time()
        i += 1
        trends[i] = t
        success.append(k)
        time.sleep(60)
    except Exception as e:
        print(e)
        exceptions.append(k)
  if len(exceptions) > 0:
    print("retrying", len(exceptions))
print(f"got interest over time")
save_trends(keycode, gprop, trends)

#%%
df_images = pd.read_csv("artist_images.csv")
visualize_trends(df_images.loc[:, :"Albrecht Dürer"])

#%%
df = pd.read_csv("artist_ngram_values.csv")
df_mid = pd.read_csv("artist_mid.csv")
df_images = pd.read_csv("artist_images.csv")
df_web = pd.read_csv("artist_web_searches.csv")

df = df.merge(df_mid, how="left", left_on="artist", right_on="artist")
df = df.drop(columns=["Unnamed: 0"], axis=1)

artists = list(df["artist"])
image_search = []
web_search = []
for i in artists:
  image_total = 0
  web_total = 0
  if i in df_images:
    image_total = df_images[i].sum()
  if i in df_web:
    web_total = df_web[i].sum()
  image_search.append(image_total)
  web_search.append(web_total)
df["images"] = image_search
df["web"] = web_search

df["scoring"] = df[["images", "web"]].mean(axis=1) * df["ngram_value"]
df.sort_values(["scoring"], ascending=False).dropna().head(10)
df.sort_values(["scoring"], ascending=True).dropna().head(10)