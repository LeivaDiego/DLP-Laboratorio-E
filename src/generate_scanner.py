from yal_processing.parse_yalex import parse_yalex
from regex_processing.regex_infix_to_postfix import infix_postfix_converter
from algorithms.direct_construction import dfa_direct_construction
from utils.write_scanner import write_scanner
from utils.path_cleaner import replace_slash_with_backslash

# This file is for generating the scanner.py file from a .yal file
raw_path = input("Enter the path of the .yal file: ")
path = replace_slash_with_backslash(raw_path)
scanner_name = (f"{path.split('/')[-1].split('.')[0]}_scanner.py")
yalex_regex, yalex_parser_code = parse_yalex(path)
postfix_yalex_regex = infix_postfix_converter(yalex_regex)
dfa = dfa_direct_construction(postfix_yalex_regex, yalex_parser_code)
write_scanner(scanner_name, postfix_yalex_regex, yalex_parser_code)