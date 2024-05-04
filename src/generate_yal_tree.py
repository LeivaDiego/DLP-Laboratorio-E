from yal_processing.parse_yalex import parse_yalex
from regex_processing.regex_infix_to_postfix import infix_postfix_converter
from algorithms.direct_construction import build_syntax_tree
from utils.show_tree import display_syntax_tree
from utils.path_cleaner import replace_slash_with_backslash

# this file is for generating the syntax tree from a .yal file
raw_path = input("Enter the path of the .yal file: ")
path = replace_slash_with_backslash(raw_path)
yalex_regex, _ = parse_yalex(path)
postfix_yalex_regex = infix_postfix_converter(yalex_regex)
yalex_expression_root, _ = build_syntax_tree(postfix_yalex_regex)
display_syntax_tree(yalex_expression_root, name=path.split("/")[-1].split(".")[0])

print("The tree has been generated successfully.")