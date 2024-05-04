import os

def replace_slash_with_backslash(path):
    """
    Replaces all occurrences of backslashes with forward slashes in the given path.

    Args:
        path (str): The path to be cleaned.

    Returns:
        str: The cleaned path with all backslashes replaced by forward slashes.
    """
    return path.replace('\\', '/')

def extract_file_name(path):
    """
    Extracts the name of the file from the given path.

    Args:
        path (str): The complete path of the file.

    Returns:
        str: The name of the file.
    """
    file_name = os.path.basename(path)
    return os.path.splitext(file_name)[0]  # Remove extension