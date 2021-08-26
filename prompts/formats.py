import random
from .grammar import valid_columns, valid_grammar, extra
# random select one from list
def format_sampler(x):
    k = random.randrange(len(x))
    return x[k]

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
            text += part[1] + part[1:].lower()  # REMBRANDT Harmenszoon van Rijn -> Rembrandt Harmenszoon van Rijn

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
    #TODO: change this if not a wga catalogue
    types = ["timeframe", "date"]

    formatting = f"{format_sampler(types)}"
    selected_fix = None
    year = data[formatting]
    text = None

    if fix == "nf":
        selected_fix = f"{format_sampler(nofix)}"
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
        k = random.randint(1, len(extra))
        selected_format = format_sampler(valid_grammar)
        if "any" in selected_format:
            selected_format = selected_format.replace("any", format_sampler(valid_columns))
        if k < len(extra):
            selected_extra = extra[k]
            if not selected_extra.split("_")[0] in selected_format:
                selected_format =f"{selected_format}-{selected_extra}"

    return selected_format

