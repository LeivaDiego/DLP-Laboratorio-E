import sys
from regex_processing.check_lexical_errors import veryfy_syntax

# Find all ocurrences of a substring in a string
find_all = lambda string, substring: [i for i in range(len(string)) if string.startswith(substring, i)]

def check_balanced_brackets(string):
    """
    Check if the given string has balanced brackets.

    Args:
        string (str): The string to check for balanced brackets.

    Returns:
        bool: True if the brackets are balanced, False otherwise.
    """
    stack = []
    brackets = {'{': '}', '[': ']'}
    for char in string:
        if char in brackets:
            stack.append(char)
        elif char in brackets.values():
            if not stack or brackets[stack.pop()] != char:
                return False
    return not stack

def read_file_lines(file_path):
    """
    Reads a file and returns a list of lines from the file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        list: A list of lines from the file, with newline characters and leading/trailing whitespace removed.
    """

    file_lines = []

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            if (line != "\n"):
                file_lines.append(line.replace("\n", "").strip())

    return file_lines


def list_to_regex(list_to_parse):
    """
    Converts a list of characters into a regular expression.

    Args:
        list_to_parse (str): The list of characters to be converted.

    Returns:
        str: The regular expression generated from the list of characters.
    """
    quotation_marks_counter = 0
    double_quotation_marks_counter = 0
    interval = False

    # check if the list has intervals
    for index, char in enumerate(list_to_parse):
        if ((char == "-") and ((index - 2) >= 0) and ((index + 2) < (len(list_to_parse) - 1))):
            interval = True
    
    step = 4 if (interval) else 2

    actual_list = []
    new_element = ""

    for char in list_to_parse:
        if (char == "'"):
            quotation_marks_counter += 1

        if (char == "\""):
            double_quotation_marks_counter += 1

        # check single quotes
        if ((quotation_marks_counter % step) != 0):
            new_element += char if (char != "'") else ""
        elif (((quotation_marks_counter % 2) == 0) and (0 < quotation_marks_counter)):
            actual_list.append(new_element)
            new_element = ""

        # check double quotes
        elif (double_quotation_marks_counter == 1):
            new_element += char if (char != "\"") else ""
        elif (double_quotation_marks_counter == 2):

            for element in list(new_element):
                actual_list.append(element)

            future_actual_list = []

            for index, element in enumerate(actual_list):

                # check for escaped characters
                if (actual_list[index - 1] == "\\"):
                    continue
                elif (element == "\\"):
                    future_actual_list.append(f"\\{actual_list[index + 1]}")
                else:
                    future_actual_list.append(element)

            actual_list = future_actual_list.copy()
            actual_list.append("")
            new_element = ""
            double_quotation_marks_counter = 0

    partial_result = actual_list[:-1]
    regex_definition = ""

    
    for index, element in enumerate(partial_result):
        if (("-" in element) and (len(element) > 2)):

            # from intervals to regex
            interval_elements = element.split("-")

            if (interval_elements[1] == ""):
                continue

            for char in range(ord(interval_elements[0]), ord(interval_elements[1]) + 1):
                regex_definition += f"{chr(char)}|"

        else:
            regex_definition += f"{element}|"

    for element in regex_definition:
        if (element in ("(", ")", "+", "?", "*")):
            regex_definition = regex_definition.replace(element, f"'{element}'")

    return regex_definition[:-1]


def get_regular_definitions(file_lines):
    """
    Parses a list of file lines and extracts regular definitions.

    Args:
        file_lines (list): A list of strings representing the lines of a file.

    Returns:
        dict: A dictionary containing the regular definitions extracted from the file.
              The keys are the names of the definitions, and the values are the corresponding regular expressions.
    """
    unparsed_regular_definitions = []

    # get regular definitions
    for line in file_lines:
        if (line.startswith("let")):
            unparsed_regular_definitions.append(line)

    regular_definitions = {}
    
    # regular definitions building
    for regular_definition in unparsed_regular_definitions:
        clean_regular_definition = regular_definition.replace("let ", "")
        key_value_definition = [string.strip() for string in clean_regular_definition.split("=")]
        if len(key_value_definition) != 2:
            sys.exit(f"Error: Invalid regular definition: {regular_definition}")
        
        if not (check_balanced_brackets(regular_definition)):
            sys.exit(f"Error: Unbalanced brackets in regular definition: {regular_definition}")

        if len(key_value_definition) != 2 or not key_value_definition[0] or not key_value_definition[1]:
            sys.exit(f"Incomplete regular definition: '{regular_definition}'. Expecting 'let identifier = definition'.")


        regular_definitions[key_value_definition[0]] = key_value_definition[1]

    for definition in regular_definitions:

        # Convert lists to regular expressions and instantiate new definition.
        if (regular_definitions[definition].startswith("[")):
            regular_definitions[definition] = list_to_regex(regular_definitions[definition])

        # possible lists to delete from the regular expression
        else:
            lists_in_definition = []
            list_to_delete = ""
            getting_list = False

            for char in regular_definitions[definition]:

                # start getting list
                if (char == "["):
                    getting_list = True

                # concat chars
                if (getting_list):
                    list_to_delete += char

                # end list
                if (char == "]"):
                    getting_list = False
                    lists_in_definition.append(list_to_delete)
                    list_to_delete = ""

            for list_to_delete in lists_in_definition:
                regular_definitions[definition] = regular_definitions[definition].replace(list_to_delete, f"({list_to_regex(list_to_delete)})")

    return regular_definitions


def get_file_initial_regex_and_tokens(file_lines):
    """
    Extracts the initial regular expression and associated tokens from a file.

    Args:
        file_lines (list): List of lines from the file.

    Returns:
        tuple: A tuple containing the initial regular expression and a list of tuples
               representing the associated code and tokens.

    """
    yalex_file_regex = ""
    building_regex = False

    for line in file_lines:

        if (line.startswith("rule")):
            building_regex = True
            continue

        if (building_regex):
            if not check_balanced_brackets(line):
                sys.exit(f"Error: Unbalanced brackets in rule: {line}")
            yalex_file_regex += line

    yalex_file_regex = list(yalex_file_regex)
    deleting_regex = False
    TO_DELETE = "ε"

    regex_actual_code = ""
    regex_associated_code = []
    getting_code = False

    for index, char in enumerate(yalex_file_regex):
        if (char == "}"):
            deleting_regex = False
            getting_code = False
            regex_associated_code.append(regex_actual_code)
            regex_actual_code = ""
            yalex_file_regex[index] = TO_DELETE

        if getting_code:
            regex_actual_code += char

        if (char == "{"):
            deleting_regex = True
            getting_code = True
            yalex_file_regex[index] = TO_DELETE

        if (yalex_file_regex[index] == "(" and yalex_file_regex[index + 1] == "*"):
            deleting_regex = True
            yalex_file_regex[index] = TO_DELETE

        if (yalex_file_regex[index] == "*" and yalex_file_regex[index + 1] == ")"):
            deleting_regex = False
            yalex_file_regex[index] = TO_DELETE
            yalex_file_regex[index + 1] = TO_DELETE

        if (deleting_regex):
            yalex_file_regex[index] = TO_DELETE

    clean_yalex_file_regex = "".join(yalex_file_regex).replace(TO_DELETE, "").split("|")
    yalex_file_regex = [char.replace(" ", "") for char in clean_yalex_file_regex]
    regex_associated_code = [token.strip() for token in regex_associated_code]

    if (yalex_file_regex.count("'") == 2):
        yalex_file_regex_copy = []
        for regex in yalex_file_regex:
            if (regex == "'"):
                continue
            else:
                yalex_file_regex_copy.append(regex)
        yalex_file_regex_copy.append("'|'")
        yalex_file_regex = yalex_file_regex_copy.copy()

    if ("return OR" in regex_associated_code):
        regex_associated_code.remove("return OR")
        regex_associated_code.append("return OR")

    regex_code_and_tokens = []
    code_return_positions = [find_all(code, "return") for code in regex_associated_code]
    token_to_return = ""

    for code, positions in zip(regex_associated_code, code_return_positions):
        for position in positions:

            RETURN_CHARACTERS = 7
            token_recognition_position = (position + RETURN_CHARACTERS)

            while ((token_recognition_position < len(code)) and (code[token_recognition_position] != " ")):
                token_to_return += code[token_recognition_position]
                token_recognition_position += 1

            regex_code_and_tokens.append((code, token_to_return))
            token_to_return = ""

    if (len(yalex_file_regex) != len(regex_code_and_tokens)):
        actual_regex_code_and_tokens = regex_code_and_tokens.copy()
        regex_code_and_tokens = []
        for entry in actual_regex_code_and_tokens:
            regex_code_and_tokens.append(entry)

    return yalex_file_regex, regex_code_and_tokens


def get_full_yalex_regex(file_regex, regular_definitions):
    """
    Applies regular definitions to the given file regex and returns the modified regex.

    Args:
        file_regex (list): A list of regular expressions.
        regular_definitions (dict): A dictionary of regular definitions.

    Returns:
        list: The modified file regex after applying regular definitions.
    """
    regex_has_regular_definitions = True

    while (regex_has_regular_definitions):

        regex_has_regular_definitions = False
        file_regex_copy = file_regex.copy()

        for index, regex in enumerate(file_regex):
            possible_regular_definitions = []

            for definition in regular_definitions:
                if (definition in regex):
                    regex_has_regular_definitions = True
                    possible_regular_definitions.append(definition)

            if (len(possible_regular_definitions) > 0):
                found_regular_definition = possible_regular_definitions[-1]
                file_regex_copy[index] = file_regex_copy[index].replace(found_regular_definition, f"({regular_definitions[found_regular_definition]})")

        file_regex = file_regex_copy.copy()

    for regex in file_regex:
        veryfy_syntax(regex)

    return file_regex


def chars_to_ascii(file_regex):
    """
    Converts characters in a regular expression to their ASCII representation.

    Args:
        file_regex (list): A list of regular expressions.

    Returns:
        list: A list of regular expressions with characters converted to ASCII.

    """
    file_regex_copy = file_regex.copy()

    for regex in file_regex_copy:
        regex_to_split = file_regex.pop(0)
        file_regex.append(list(regex_to_split))

    file_regex_copy = file_regex.copy()

    # ASCII conversion of the regular expression.
    for regex in file_regex:

        regex_copy = []
        file_regex_copy.remove(regex)

        on_double_quotes = False

        for jndex, char in enumerate(regex):
            if (jndex < (len(regex) - 1) and (char in ("(", ")", "+", "?", "*", "|")) and (regex[jndex - 1] == "'") and (regex[jndex + 1] == "'")):
                regex_copy.append(str(ord(char)))

            elif (regex[jndex - 1] == "\\"):
                regex_copy.pop()
                if (char == "n"):
                    regex_copy.append(str(ord("\n")))
                elif (char == "t"):
                    regex_copy.append(str(ord("\t")))
                elif (char == "r"):
                    regex_copy.append(str(ord("\r")))
                elif (char == "f"):
                    regex_copy.append(str(ord("\f")))
                elif (char == "v"):
                    regex_copy.append(str(ord("\v")))
                elif (char == "b"):
                    regex_copy.append(str(ord("\b")))
                elif (char == "a"):
                    regex_copy.append(str(ord("\a")))
                elif (char == "0"):
                    regex_copy.append(str(ord("\0")))
                elif (char == "s"):
                    regex_copy.append(str(ord(" ")))

            elif (char in ("(", ")", "+", "?", "*", "|")):
                regex_copy.append(char)

            elif (char == "'"):
                continue

            elif ((char == "\"") and (not on_double_quotes)):
                on_double_quotes = True
                regex_copy.append("(")
                continue

            elif ((char == "\"") and (on_double_quotes)):
                on_double_quotes = False
                regex_copy.append(")")
                continue

            else:
                regex_copy.append(str(ord(char)))

        file_regex_copy.append(regex_copy)

    regex_token_position = 0

    for regex in file_regex_copy:
        regex.append(f"#{regex_token_position}")
        regex_token_position += 1

    return file_regex_copy


def finish_file_regex(file_regex):
    """
    Finish the file regex by converting subexpressions to a single list of characters,
    removing unnecessary characters, and returning the final regular expression.

    Args:
        file_regex (list): A list of subexpressions.

    Returns:
        list: The final regular expression as a list of characters.
    """
    file_regex_copy = file_regex.copy()
    file_regex = []

    for regex in file_regex_copy:
        for char in regex:
            file_regex.append(char)
        file_regex.append("|")

    file_regex.pop()

    file_regex_copy = file_regex.copy()
    file_regex = []

    for char in file_regex_copy:
        if (char != "92"):
            file_regex.append(char)

    return file_regex

def parse_yalex(path):
    """
    Parses a YALEX file and returns the complete regular expression and the associated tokens.

    Args:
        path (str): The path to the YALEX file.

    Returns:
        tuple: A tuple containing the complete regular expression and the associated tokens.

    """
    file_lines = read_file_lines(path)
    regular_definitions = get_regular_definitions(file_lines)
    file_regex, regex_code_and_tokens = get_file_initial_regex_and_tokens(file_lines)
    complete_file_regex = get_full_yalex_regex(file_regex, regular_definitions)
    complete_file_regex = chars_to_ascii(complete_file_regex)
    complete_file_regex = finish_file_regex(complete_file_regex)

    return complete_file_regex, regex_code_and_tokens