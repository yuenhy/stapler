import random
from .grammar import *
from .custom_strings import *

# random select one from list
def format_sampler(x):
    k = random.sample(x, 1)
    return k[0]

def get_custom_vertical(data):
    # random select one from list
    text = format_sampler(data)
    return text

def get_custom_horizontal(counter, data):
    # select by position index
    if counter >= len(data):
        return None
    text = data[counter]
    return text

def get_custom_format(counter, f, data, prompt_format):
    text = None
    try:
        if f == custom_flag:
            # randomized data
            text = get_custom_horizontal(counter, data)
        else:
            # get list from grammar.py
            custom = eval(f)
            if change_axis:
                text = get_custom_vertical(custom)
            else:
                text = get_custom_horizontal(counter, custom)
                if text is None:
                    raise Exception(f"{f} has {len(custom)} value(s) but you specified at least {counter+1} flags in {prompt_format}")
    except NameError as e:
        raise Exception(f"{f} not in custom_strings.py")
    
    formatting = f
    return text, formatting, counter + 1


def get_author_format(fix, data):
    prefix = ["in_style_of", "by"]
    suffix = ["s"]
    nofix = ["no_extra"]
    # afix = [""]
    types = ["lname", "fullname"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    parts = data.split(",")
    try:
        if len(parts) == 1: # ARCANGELO DI JACOPO DEL SELLAIO
            raise Exception("use fullname")

        lname = parts[0][0] + parts[0][1:].lower()
        fname = "".join(parts[1:]).strip()
        
        if formatting == "lname":
            text = lname
        elif formatting == "fullname":
            text = f"{fname} {lname}"
    except Exception as e:
        formatting = "fullname"
        name = data.split(" ")
        text = ""
        for part in name:                       # ARCANGELO DI JACOPO DEL SELLAIO -> Arcangelo Di Jacopo Del Sellaio
            text += str(part[0]) + str(part[1:]).lower() + " "  # REMBRANDT Harmenszoon van Rijn -> Rembrandt Harmenszoon van Rijn
        text.strip()
    if fix == "nf":
        selected_fix = format_sampler(nofix)
    elif fix == "pf":
        selected_fix = format_sampler(prefix).replace("_", " ")
        text = f"{selected_fix} {text}"
    elif fix == "sf":
        # 's
        selected_fix = format_sampler(suffix)
        text = f"{text}'{selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({text})"

    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_bd_format(fix, data):
    nofix = ["no_extra"]
    types = ["bd"]
    
    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_year_format(fix, data):
    prefix = ["in", "around"]
    afix = ["parenthesis"]
    nofix = ["no_extra"]
    #change this as required
    types = ["timeframe", "date"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    year = data[formatting]
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = year
    elif fix == "pf":
        selected_fix = f"{format_sampler(prefix)}"
        text = f"{selected_fix} {year}"
    # elif fix == "sf":
    #     selected_fix = f"{format_sampler(suffix)}"
    #     text = "{year} {selected_fix}"
    elif fix == "af":
        selected_fix = f"{format_sampler(afix)}"
        if selected_fix == "parenthesis":
            text = f"({year})"
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_technique_format(fix, data):
    nofix = ["no_extra"]
    types = ["technique"]
    
    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    # elif fix == "pf":
    #     selected_fix = format_sampler(prefix).replace("_", " ")
    #     text = f"{selected_fix} {data}"
    # elif fix == "sf":
    #     selected_fix = format_sampler(suffix).replace("_", " ")
    #     text = f"{data} {selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({data})"

    formatting = f"{formatting}_{selected_fix}"

    return text, formatting

def get_location_format(fix, data):
    nofix = ["no_extra"]
    prefix = ["in", "at", "from"]
    types = ["location"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    elif fix == "pf":
        selected_fix = f"{format_sampler(prefix).replace('_', ' ')}"
        text = f"{selected_fix} {data}"
    # elif fix == "sf":
    #     selected_fix = format_sampler(suffix).replace("_", " ")
    #     text = f"{data} {selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({data})"
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_form_format(fix, data):
    nofix = ["no_extra"]
    types = ["form"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    # elif fix == "pf":
    #     selected_fix = format_sampler(prefix).replace("_", " ")
    #     text = f"{selected_fix} {data}"
    # elif fix == "sf":
    #     selected_fix = format_sampler(suffix).replace("_", " ")
    #     text = f"{data} {selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({data})"
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_type_format(fix, data):
    nofix = ["no_extra"]
    types = ["type"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    # elif fix == "pf":
    #     selected_fix = format_sampler(prefix).replace("_", " ")
    #     text = f"{selected_fix} {data}"
    # elif fix == "sf":
    #     selected_fix = format_sampler(suffix).replace("_", " ")
    #     text = f"{data} {selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({data})"
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_school_format(fix, data):
    nofix = ["no_extra"]
    types = ["school"]
    
    formatting = f"{format_sampler(types)}"
    selected_fix = None
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
        text = data
    # elif fix == "pf":
    #     selected_fix = format_sampler(prefix).replace("_", " ")
    #     text = f"{selected_fix} {data}"
    # elif fix == "sf":
    #     selected_fix = format_sampler(suffix).replace("_", " ")
    #     text = f"{data} {selected_fix}"
    # elif fix == "af":
    #     selected_fix = f"{format_sampler(afix)}"
    #     if selected_fix == "parenthesis":
    #         text = f"({data})"
    
    formatting = f"{formatting}_{selected_fix}"
    
    return text, formatting

def get_prompt_format(use_custom=False):
    #TODO: use_custom
    # year is DATE or TIMEFRAME

    if not use_custom:
        # use extra stuff or no
        k = random.randint(0, len(extra))
        selected_format = format_sampler(valid_grammar)
        if "any_" in selected_format:
            selected_format = selected_format.replace("any_", f"{format_sampler(valid_columns)}_")
        if k < len(extra):
            selected_extra = extra[k]
            if not selected_extra.split("_")[0] in selected_format:
                selected_format = f"{selected_format}-{selected_extra}"


    return selected_format

