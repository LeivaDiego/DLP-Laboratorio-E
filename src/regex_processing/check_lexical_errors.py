import sys

OPERATORS = ("+", "?", "*", ".", "|")

def veryfy_syntax(regex):
    """
    Verifies the syntax of a regular expression.

    Parameters:
    regex (str): The regular expression to be verified.

    Raises:
    SystemExit: If the regular expression is invalid, specific error messages are raised.

    Returns:
    None
    """
    # check if the regex is a single character
    if ((regex == "'('") or (regex == "')'")):
        return

    # check if the regex is empty
    if ((regex == "") or (regex == [])):
        sys.exit(f"Error: The regex \"{regex}\" can't be empty.")

    # Check if theres invalid or operator at the end
    if (regex[-1] == "|"):
        sys.exit(f"Error: The regex \"{regex}\" can't end with a \"|\" operator.")

    # Check if theres invalid operator at the start
    for operator in OPERATORS:
        if ((regex == operator) or (regex == [operator]) or (regex == ["(", operator, ")"])):
            sys.exit(f"Error: The regex \"{regex}\" can't be only a \"{operator}\" operator.")
        elif (regex[0] == operator):
            sys.exit(f"Error: The regex \"{regex}\" can't start with a \"{operator}\" operator.")

    # Count of parenthesis
    left_parenthesis = regex.count("(")
    right_parenthesis = regex.count(")")

    # Check if parenthesis are balanced
    if (left_parenthesis != right_parenthesis):
        sys.exit(f"Error: The regex \"{regex}\" has a wrong number of parenthesis.")


    only_parenthesis = True

    for char in regex:
        if char not in ("(", ")"):
            only_parenthesis = False
            break

    # Check if the regex is only parenthesis
    if (only_parenthesis):
        sys.exit(f"Error: The regex \"{regex}\" can't be only parenthesis.")

    
    for i in reversed(range(1, len(regex))):
        if ((regex[i] in OPERATORS) and (regex[i - 1] == "|")):
            sys.exit(f"Error: The regex \"{regex}\" has a wrong operator placement at indexes {i - 1} and {i}.")
