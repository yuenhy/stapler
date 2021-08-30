from .grammar import custom_flag
#####################################################################
# custom_flag = "cus" change this in grammar.py
# if change_axis == False
#
# "cus_0-year_nf-form_nf-cus_0" will check for cus_0, and greedily inject from cus_0
# a photo of a 1700 painting in 8K ULTRA HD
#
# `cus` without additional specification
# "cus-year_nf-form_nf" will check for any cus_x, where len(cus_x) == number of custom flags found in format
# format.count(custom_flag) == 1, so cus_1a OR cus_1b 
# a zipped file of a 1700 painting OR the non-compressed version of a 1700 painting
# 
#####################################################################
# custom_flag = "cus" change this in grammar.py
# if change_axis == True
#
# "year_nf-cus_colors-form_nf-cus_types" will sample and inject from cus_colors and cus_4 accordingly
# 1700 blue painting BDR
#
# `cus` not allowed
#####################################################################

# avoid using <custom_flag> in list name
# should follow <custom_flag>_listOfStrings 
cusz_0 = ["a photo of a", "in 8K ULTRA HD"]
cusz_1a = ["a zipped file of a"]
cusz_1b = ["the non-compressed version of a"]
cusz_color = ["red", "blue"]
cusz_type = ["BDR", "WEB-DL", "CAM-Rip"]




#####################################################################
custom_all_strings = {} # if renaming, update generator.py > parse_format() as well
for name in dir():
    if not name.startswith('__'):
    # if not name.startswith('__') and type(name) == list:
        actual = eval(name)
        if type(actual) is list:
            if name == custom_flag:
                raise Exception("list name == custom flag not allowed")
            elif not "_" in name:
                raise Exception(f"{name} not allowed, please follow list naming convention")
            elif not f"{custom_flag}_" in name:
                raise Exception(f"{name} not allowed, please start list name with `{custom_flag}_`")
            elif name.count("_") > 1:
                raise Exception(f"{name} not allowed, use camelCase instead")
            elif name.count(custom_flag) > 1:
                raise Exception(f"{name} not allowed, avoid using flag in list name")
            length = len(actual)
            if length == 0:
                raise Exception(f"{name} is empty")
            if length in custom_all_strings:
                custom_all_strings[length].append(actual)
            else:
                custom_all_strings[length] = [actual]

