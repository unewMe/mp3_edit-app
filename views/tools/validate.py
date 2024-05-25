from typing import re


def is_valid_filename(filename):
    invalid_chars = '<>:"/\\|?*'

    reserved_names_regex = r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)'

    if any(char in invalid_chars for char in filename):
        return False

    if re.match(reserved_names_regex, filename, re.IGNORECASE):
        return False
    return True

