import re

def clean_filename(filename: str) -> str:
    """
    Clean up the filename by converting it to lowercase and replacing spaces with hyphens.
    """
    cleaned_name = filename.lower()
    cleaned_name = re.sub(r'\s+', '-', cleaned_name)
    return cleaned_name