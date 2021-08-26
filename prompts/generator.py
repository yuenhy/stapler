from .formats import *
import pandas as pd

# parse prompt format
def parse_format(row, prompt_format):
    prompt = ""
    final_format = ""
    text = None
    formatting = None
    for f in prompt_format.split("-"):
        col, fix = f.split("_")
        # valid_columns = ["author", "bd", "year", "technique", "location", "form", "type", "school"]
        if col == "author":
            text, formatting = get_author_format(fix, row.AUTHOR)
        elif col == "bd":
            # BORN-DIED
            text, formatting = get_bd_format(fix, row._2)
        elif col == "year":
            # TODO: to edit formats.py > get_year_formats()
            # and grammar.py > valid_columns
            years = {
                "timeframe": row.TIMEFRAME,
                "date": row.DATE
            }
            text, formatting = get_year_format(fix, years)
        elif col == "technique":
            text, formatting = get_technique_format(fix, row.TECHNIQUE)
        elif col == "location":
            text, formatting = get_location_format(fix, row.LOCATION)
        elif col == "form":
            text, formatting = get_form_format(fix, row.FORM)
        elif col == "type":
            text, formatting = get_type_format(fix, row.TYPE)
        elif col == "school":
            text, formatting = get_school_format(fix, row.SCHOOL)
        else:
            print(col, fix)
            raise Exception("check grammar")
        
        if not text is None and not text == "other":
            prompt = f"{prompt} {text}"
            final_format = f"{final_format}-{formatting}"
    
    return prompt.strip(), final_format[1:]

def export_list(prompt_list, filename):
    print("saved to", filename)
    df = pd.DataFrame(prompt_list, columns=["REF_ID", "PROMPT", "PROMPT_FORMAT", "START_LATENT", "GENERATED_IMG", "REFERENCE_IMG"])
    df.to_csv(filename, index=False)

# pp, runs
# run each prompt 5 times
def get_prompt_ref_list(df, pp, runs, filename):

    prompt_list = []
    unique_prompts = []

    for row in df.itertuples():
        for i in range(pp):
            prompt_format = get_prompt_format()
            prompt, final_format = parse_format(row, prompt_format)
            start_latent = f"{row.ID}.backup"
            reference_img = "_".join(row.URL.split("/")[5:]).replace("html", "jpg")
            unique_prompts.append(prompt)
            for j in range(runs):
                generated_img = f"{row.ID}-{i}-{j}.png"
                #columns=["REF_ID", "PROMPT", "PROMPT_FORMAT", "START_LATENT", "GENERATED_IMG", "REFERENCE_IMG"]
                prompt_list.append([row.ID, prompt, final_format, start_latent, generated_img, reference_img])
    export_list(prompt_list, filename)
    return unique_prompts

# aw, pp, runs
# for 50 artworks, make 5 prompts
# run each prompt 5 times
def make_prompts(csv, filename="prompt_reference_list.csv", aw=50, pp=5, runs=5):
    df = pd.read_csv(csv)
    df = df.assign(AUTHOR_ID=(df.AUTHOR).astype("category").cat.codes)
    df = df.assign(ROW_ID=(df.URL).astype("category").cat.codes)
    df["ID"] = df["AUTHOR_ID"].astype(str) +"-"+ df["ROW_ID"].astype(str)
    df.drop(columns=["AUTHOR_ID", "ROW_ID"], inplace=True)

    df_sampled = pd.DataFrame()
    if aw:
        df_sampled = df.sample(int(aw))
    elif aw is False:
        df_sampled = df.copy()

    unique_prompts = get_prompt_ref_list(df_sampled, pp, runs, filename)

    return unique_prompts


