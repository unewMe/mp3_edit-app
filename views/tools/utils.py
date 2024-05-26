import re

_FILE_EXTENSIONS = ['mp3']


def is_valid_filename(filename: str) -> bool:
    """Check if a filename is valid."""
    invalid_chars = '<>:"/\\|?*'

    reserved_names_regex = r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)'

    if any(char in invalid_chars for char in filename):
        return False

    if re.match(reserved_names_regex, filename, re.IGNORECASE):
        return False
    return True
