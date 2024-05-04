from yal_processing.parse_yalp import parse_yalp, verify_yalex_tokens
from yal_processing.parse_yalex import parse_yalex
from utils.path_cleaner import replace_slash_with_backslash

yalex_raw = input("Enter the path of the .yal file: ")
yalex_path = replace_slash_with_backslash(yalex_raw)

yalp_raw = input("Enter the path of the .yalp file: ")
yalp_path = replace_slash_with_backslash(yalp_raw)

try:
    _, yalex_parser_code = parse_yalex(yalex_path)
    tokens, productions = parse_yalp(yalp_path)
    verify_yalex_tokens(yalex_parser_code, tokens)
except Exception as e:
    print(f"ERROR: {e}")