from models.stack import Stack

OPERATORS = ("+", "?", "*", ".", "|")
OPERATORS_AND_PARENTHESIS = ("(", ")", "+", "?", "*", ".", "|")
OPERATOR_PRECEDENCE = { "+": 3, "?": 3, "*": 3, ".": 2, "|": 1, "(": 0, ")": 0, "": 0 }
IMPOSSIBLY_HIGH_PRECEDENCE = 99

def apply_concat(regex):
    """
    Checks for concatenations in a regular expression and returns the converted regular expression.

    Args:
        regex (str): The regular expression to check for concatenations.

    Returns:
        list: The converted regular expression with concatenations.

    """
    output = []

    for index, char in enumerate(regex):
        output.append(char)

        # check for valir operators for explicit concat
        if ((char == "|") or (char == "(") or (char == ".")):
            continue

        elif ((index < (len(regex) - 1)) and ((char in (")", "+", "?", "*")) or (char not in OPERATORS_AND_PARENTHESIS)) and (regex[index + 1] not in ("+", "?", "*", "|", ")"))):
            output.append(".")

    return output

def infix_postfix_converter(regex):
    """
    Converts an infix regular expression to postfix notation.

    Args:
        regex (str): The infix regular expression to convert.

    Returns:
        list: The postfix expression as a list of tokens.

    """
    regex = apply_concat(regex)

    postfix = []
    operator_stack = Stack()

    for char in regex:
        if (char == "("):
            operator_stack.push(char)
        elif (char == ")"):
            while (operator_stack.peek() and (operator_stack.peek() != "(")):
                postfix.append(operator_stack.pop())
            operator_stack.pop()

        else:
            while (not operator_stack.is_empty()):
                peeked_char = operator_stack.peek()
                peeked_precedence = OPERATOR_PRECEDENCE.get(peeked_char, IMPOSSIBLY_HIGH_PRECEDENCE)
                char_precedence = OPERATOR_PRECEDENCE.get(char, IMPOSSIBLY_HIGH_PRECEDENCE)

                if (peeked_precedence >= char_precedence):
                    postfix.append(operator_stack.pop())

                else:
                    break

            operator_stack.push(char)

    while (not operator_stack.is_empty()):
        postfix.append(operator_stack.pop())

    return postfix