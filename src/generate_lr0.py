from yal_processing.parse_yalp import parse_yalp
from utils.path_cleaner import replace_slash_with_backslash

raw_path = input("Enter the path of the .yal file: ")
path = replace_slash_with_backslash(raw_path)

try:
    tokens, productions = parse_yalp(path)
except Exception as e:
    print(f"Error: {e}")