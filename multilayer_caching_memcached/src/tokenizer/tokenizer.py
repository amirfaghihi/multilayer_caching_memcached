import re


def standard_tokenizer(in_string: str):
    return re.split(', |\. |-|_| |@|\!|\?|\: |\، ', in_string.rstrip("\?\.\!"))
