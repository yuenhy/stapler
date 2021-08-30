# this is made specifically for wga catalogue
# so year might be DATE or TIMEFRAME
valid_columns = ["author", "bd", "year", "technique", "location", "form", "type", "school"]

# nofix - nf - `no_extra` formatting
# prefix - pf - prepend word(s)
# suffix - sf - append word(s)
# afix - af - prepend & append, e.g. parenthesis
# separate column item by dashes 
# specify extra formatting with underscores
valid_grammar = [
    "year_nf-form_nf", # 1700 painting
    "author_nf-form_nf", # bartolomeo painting
    "school_nf-form_nf", # italian architecture
    "type_nf-form_nf", # religious sculpture
    "type_nf-technique_nf", # religious marble
    "school_nf-type_nf-form_nf", # german mythological painting
    "school_nf-type_nf-form_nf-author_pf", # german mythological painting by zwirner
    "school_nf-type_nf-form_nf-author_pf-year_af", # german mythological painting by zwirner (1839)
    "school_nf-type_nf-form_nf-author_pf-year_af-bd_nf", # german mythological painting by zwirner (b. 1802, Jakobswalde, d. 1861, Köln)
    # # "any_nf", # any one 
    "school_nf-cusz_color-type_nf-form_nf-author_pf-year_af-cusz_type", 
    # "cusz_0-year_nf-form_nf-cusz_0" # a photo of a 1700 painting in 8K ULTRA HD 
]

# extra stuff to possibly attach to valid grammar
# add to valid_grammar to force 
# will not repeat if column item exists in prompt e.g. invalid_grammer = ["year_nf-form_nf-year_nf"]
extra = ["year_af", "location_pf"]
# "school_nf-form_nf-location_pf", # italian architecture from boboli gardens
# "type_nf-form_nf-location_pf", # religious sculpture from kunsthistorisches museum
# "school_nf-type_nf-form_nf-location_pf", # german mythological painting in the hermitage
# "school_nf-type_nf-form_nf-author_pf-year_af", # german mythological painting by zwirner (1839)

#########################################
# check custom_strings.py for examples
custom_flag = "cusz"
# use cus_x when writing valid grammar to specify a list

# check custom_strings.py for examples
change_axis = True
# False, horizontal 
# x y if [x, y]
# True, vertical
# x k if [x, y] [j, k]