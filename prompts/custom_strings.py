from .grammar import custom_flag

#####################################################################
# Add custom string lists to the dict below.
# Each key must follow the pattern  <custom_flag>_listName  (e.g. "var_0").
# Use camelCase for multi-word names: "var_myList", not "var_my_list".
#
# horizontal fill  (change_axis = False in grammar.py)
#
#   "var_0-year_nf-form_nf-var_0"
#   → greedily pulls from var_0 by position
#   → "a photo of a 1700 painting in 8K ULTRA HD"
#
#   "var-year_nf-form_nf"
#   → picks any list whose length equals the number of var tokens (1 here)
#   → "a zipped file of a 1700 painting"  OR
#      "the non-compressed version of a 1700 painting"
#
# vertical fill  (change_axis = True in grammar.py)
#
#   "year_nf-var_color-form_nf-var_type"
#   → samples one entry from each named list independently
#   → "1700 blue painting BDR"
#   (unsubscripted `var` is not allowed in vertical mode)
#####################################################################

custom_strings: dict[str, list[str]] = {
    "var_0":     ["a photo of a", "in 8K ULTRA HD"],
    "var_1a":    ["a zipped file of a"],
    "var_1b":    ["the non-compressed version of a"],
    "var_color": ["red", "blue"],
    "var_type":  ["BDR", "WEB-DL", "CAM-Rip"],
}

#####################################################################
# Validation — checked once at import time.
#####################################################################
for _name, _strings in custom_strings.items():
    if _name == custom_flag:
        raise ValueError(f"list name cannot equal the custom flag '{custom_flag}'")
    if "_" not in _name:
        raise ValueError(f"'{_name}' must follow naming convention: {custom_flag}_listName")
    if not _name.startswith(f"{custom_flag}_"):
        raise ValueError(f"'{_name}' must start with '{custom_flag}_'")
    if _name.count("_") > 1:
        raise ValueError(f"'{_name}' has too many underscores — use camelCase after the prefix (e.g. {custom_flag}_myList)")
    if _name.count(custom_flag) > 1:
        raise ValueError(f"'{_name}' — avoid repeating the flag in the list name")
    if len(_strings) == 0:
        raise ValueError(f"'{_name}' is empty")

#####################################################################
# Build the count-indexed lookup used by generator.py when the
# prompt format contains an unsubscripted var token.
# Maps  list_length → [list, list, ...]  so the caller can pick any
# list whose length matches the number of var slots in the format.
#####################################################################
custom_all_strings: dict[int, list[list[str]]] = {}
for _strings in custom_strings.values():
    custom_all_strings.setdefault(len(_strings), []).append(_strings)
