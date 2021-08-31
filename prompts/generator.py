from .formats import *
import pandas as pd

# parse prompt format
def parse_format(row, prompt_format):
    prompt = []
    final_format = ""
    text = None
    formatting = None

    data = {
        "author":row.AUTHOR,
        # BORN-DIED
        "bd": row._2,
        "year":{
            "timeframe": row.TIMEFRAME,
            "date": row.DATE,
        },
        "technique": row.TECHNIQUE,
        "location": row.LOCATION,
        "form": row.FORM,
        "type": row.TYPE,
        "school": row.SCHOOL
    }

    # check if custom flag is specified correctly
    custom_count = prompt_format.count(custom_flag)
    specified_count = prompt_format.count(f"{custom_flag}_")
    if specified_count > 0 and custom_count + specified_count > specified_count * 2:
        raise Exception(f"inconsistent flag use in {prompt_format}")

    # counter for indexing in horizontal fill
    custom_counter = 0
    custom_random = False
    custom_data = []
    # for randomization
    if custom_count in custom_all_strings:
        custom_data = format_sampler(custom_all_strings[custom_count])

    for f in prompt_format.split("-"):
        parts = f.split("_")
        col = parts[0]
        fix = None
        
        if len(parts) == 2:
            col, fix = parts
        elif not col == custom_flag:
            raise Exception("{col} not recognized as custom flag, check grammar")
        elif len(parts) > 2:
            raise Exception(f"{prompt_format} cannot be parsed, check grammar")
        if col == custom_flag and fix is None:
            custom_random = True
        if custom_random and change_axis:
            raise Exception("vertical custom sampling requires a specified list, check change_axis in grammar.py")        

        if col == "author":
            text, formatting = get_author_format(fix, data["author"])
        elif col == "bd":
            text, formatting = get_bd_format(fix, data["bd"])
        elif col == "year":
            text, formatting = get_year_format(fix, data["year"])
        elif col == "technique":
            text, formatting = get_technique_format(fix, data["technique"])
        elif col == "location":
            text, formatting = get_location_format(fix, data["location"])
        elif col == "form":
            text, formatting = get_form_format(fix, data["form"])
        elif col == "type":
            text, formatting = get_type_format(fix, data["type"])
        elif col == "school":
            text, formatting = get_school_format(fix, data["school"])
        elif col == custom_flag:
            if custom_random and not fix is None:
                raise Exception("if you would like to randomize strings from specific lists try change_axis == True")
            elif not custom_random and fix is None:
                raise Exception(f"inconsistent {prompt_format}")
            text, formatting, custom_counter = get_custom_format(custom_counter, f, custom_data, prompt_format)
        else:
            raise Exception(f"{f} not recognized, check grammar")

        if text is None:
            # e.g. school_pf, but prefix is not declared
            raise Exception(f"{f} not recognized, check formats")

        if not text is None and not text == "other":
            # return prompt in list format
            prompt.append(text.strip())
            final_format = f"{final_format}-{formatting}"

    return prompt, final_format[1:]

def export_list(prompt_list, filename):
    print("saved to", filename)
    df = pd.DataFrame(prompt_list, columns=["REF_ID", "PROMPT", "PROMPT_FORMAT", "START_LATENT", "GENERATED_IMG", "REFERENCE_IMG"])
    df.to_csv(filename, index=False)

# pp, runs
# run each prompt 5 times
def get_prompt_ref_list(df, pp, runs, filename):

    prompt_list = []
    unique_prompts = []

    latent_file_ext = "pkl"

    for row in df.itertuples():
        for i in range(pp):
            j = i
            prompt_format = get_prompt_format(j) # use valid_grammar sequentially and wrap around
            # prompt_format = get_prompt_format() # random sample with replacement

            prompt, final_format = parse_format(row, prompt_format)
            # https://www.wga.hu/html_m/l/le_brun/1versail/6other1.html -> le_brun_1versail_6other1.jpg
            reference_img = "_".join(row.URL.split("/")[5:]).replace("html", "jpg")
            unique_prompts.append(prompt)
            for j in range(runs):
                start_latent = f"{row.ID}-{j}.{latent_file_ext}"
                generated_img = f"{row.ID}-{i}-{j}.png"
                #columns=["REF_ID", "PROMPT", "PROMPT_FORMAT", "START_LATENT", "GENERATED_IMG", "REFERENCE_IMG"]
                prompt_list.append([row.ID, prompt, final_format, start_latent, generated_img, reference_img])
    if filename:
        export_list(prompt_list, filename)
    return unique_prompts

# aw, pp, runs
# for 50 artworks, make 5 prompts
# run each prompt 5 times
def make_prompts(csv, filename=None, aw=50, pp=5, runs=5):
    df = pd.read_csv(csv)
    df = df.assign(AUTHOR_ID=(df.AUTHOR).astype("category").cat.codes)
    df = df.assign(ROW_ID=(df.URL).astype("category").cat.codes)
    df["ID"] = df["AUTHOR_ID"].astype(str) +"-"+ df["ROW_ID"].astype(str)
    df.drop(columns=["AUTHOR_ID", "ROW_ID"], inplace=True)

    custom = {
        "group0": ["VERESHCHAGIN, Vasily Petrovich", "HAYEZ, Francesco", "ZURBARÁN, Francisco de", "LIMBOURG brothers", "FRAGONARD, Jean-Honoré"],
        "group1": ["PRENDERGAST, Maurice Brazil", "CAILLEBOTTE, Gustave", "ALTDORFER, Albrecht", "JORDAENS, Jacob",  "VERMEER, Johannes"],
        "group2": ["SEURAT, Georges", "MEMLING, Hans", "COURBET, Gustave", "WHISTLER, James Abbot McNeill", "MILLAIS, Sir John Everett"],
        "group3": ["PARMIGIANINO", "RAFFAELLO Sanzio", "AIVAZOVSKY, Ivan Konstantinovich", "BOSCH, Hieronymus", "BELLOTTO, Bernardo"]
    }
    max_pieces = 6

    df_sampled = pd.DataFrame(columns=df.columns)
    if aw in custom:
        print("found custom group")
        for i in custom[aw]:
            df_artist = df[df.AUTHOR.isin(custom[aw])]
            if len(df_artist) > max_pieces:
                df_artist = df_artist.sample(max_pieces)
        df_sampled = df_sampled.append(df_artist)
    elif aw:
        df_sampled = df.sample(int(aw))
 
    elif aw is False:
        df_sampled = df.copy()

    unique_prompts = get_prompt_ref_list(df_sampled, pp, runs, filename)

    return unique_prompts


