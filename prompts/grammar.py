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
    # "any_nf", # any one 
]

# extra stuff to possibly attach to valid grammar
# add to valid_grammar to force 
# will not repeat if column item exists in prompt
extra = ["year_af", "location_pf"]
# e.g.
# "school-nf_form-nf-location-pf", # italian architecture from boboli gardens
# "type-nf-form_nf-location-pf", # religious sculpture from kunsthistorisches museum
# "school-nf_type-nf-form_nf-location-pf", # german mythological painting in the hermitage
# "school_nf-type_nf-form_nf-author_pf-year_af", # german mythological painting by zwirner (1839)