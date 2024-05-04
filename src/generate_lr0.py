from yal_processing.parse_yalp import parse_yalp, verify_yalex_tokens
from yal_processing.parse_yalex import parse_yalex
from utils.path_cleaner import replace_slash_with_backslash, extract_file_name
from models.grammar import *
from models.lr0 import *

yalex_raw = input("Enter the path of the .yal file: ")
yalex_path = replace_slash_with_backslash(yalex_raw)

yalp_raw = input("Enter the path of the .yalp file: ")
yalp_path = replace_slash_with_backslash(yalp_raw)

file_name = extract_file_name(yalp_path)
try:
    _, yalex_parser_code = parse_yalex(yalex_path)
    tokens, productions = parse_yalp(yalp_path)
    verify_yalex_tokens(yalex_parser_code, tokens)
    grammar_str = dict_to_grammar_str(productions)
    grammar = Grammar(grammar_str)
    slr_parser = SLRParser(grammar)
    slr_parser.generate_automaton(file_name)
except Exception as e:
    print(f"ERROR: {e}")