def replace_slash_with_backslash(path):
    """
    Replaces all occurrences of backslashes with forward slashes in the given path.

    Args:
        path (str): The path to be cleaned.

    Returns:
        str: The cleaned path with all backslashes replaced by forward slashes.
    """
    return path.replace('\\', '/')