import re


def pascal_to_snake_case(string):
    return "_".join(re.findall("[A-Z]{1}[a-z]*", string)).lower()
