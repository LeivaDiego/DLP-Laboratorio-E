from regex_processing.regex_infix_to_postfix import OPERATORS
from models.node import Node
from models.stack import Stack
from models.dfa import DFA

def build_syntax_tree(postfix):
    """
    Builds a syntax tree from a postfix expression.

    Args:
        postfix (list): A list representing the postfix expression.

    Returns:
        tuple: A tuple containing the root node of the syntax tree and an array of nodes.
    """

    if (f"{postfix[-2]}{postfix[-1]}" != "35."):
        postfix.append("35")
        postfix.append(".")

    node_stack = Stack()
    node_array = []
    position = 1

    for char in postfix:
        # Kleene star operator node construction
        if (char == "*"):
            operand = node_stack.pop()
            node = Node(char)
            node.left = operand
            node_stack.push(node)
            node_array.append(node)

        # Plus operator node construction
        elif (char == "+"):
            operand = node_stack.pop()
            node = Node(char)
            node.left = operand
            node_stack.push(node)
            node_array.append(node)

        # Question mark operator node construction
        elif (char == "?"):
            operand = node_stack.pop()
            node = Node(char)
            node.left = operand
            node_stack.push(node)
            node_array.append(node)

        # Concat operator node construction
        elif (char == "."):
            right_operand = node_stack.pop()
            left_operand = node_stack.pop()
            node = Node(char)
            node.left = left_operand
            node.right = right_operand
            node_stack.push(node)
            node_array.append(node)

        # Or operator node construction
        elif (char == "|"):
            right_operand = node_stack.pop()
            left_operand = node_stack.pop()
            node = Node(char)
            node.left = left_operand
            node.right = right_operand
            node_stack.push(node)
            node_array.append(node)

        # Tree leaf node construction
        else:
            node = Node(char, position)
            node_stack.push(node)
            node_array.append(node)
            position += 1

    # Return the root node of the syntax tree and the array of nodes.
    return node_stack.pop(), node_array


def nullable(node):
    """
    Determines if a given node in a syntax tree is nullable.

    Args:
        node (Node): The node to check for nullability.

    Returns:
        bool: True if the node is nullable, False otherwise.
    """
    if (type(node) != Node):
        return False

    if ((type(node) == Node) and (node.left == None) and (node.right == None)):
        return (node.value == "ε")

    else:
        if (node.value == "*"):
            return True
        elif (node.value == "+"):
            return nullable(node.left)
        elif (node.value == "?"):
            return True
        elif (node.value == "."):
            return (nullable(node.left) and nullable(node.right))
        elif (node.value == "|"):
            return (nullable(node.left) or nullable(node.right))


def firstpos(node):
    """
        Calculates the firstpos set for a given node in a syntax tree.

        Args:
            node (Node): The node for which to calculate the firstpos set.

        Returns:
            set: The firstpos set for the given node.
    """
    if (type(node) != Node):
        return set()

    # Base case, 1 node.
    if ((node.left == None) and (node.right == None)):
        if (node.value == "ε"):
            return set()
        else:
            return { node }

    # Inductive case, 2 nodes.
    else:
        if (node.value == "*"):
            return firstpos(node.left)
        elif (node.value == "+"):
            return firstpos(node.left)
        elif (node.value == "?"):
            return firstpos(node.left)
        elif (node.value == "."):
            if (nullable(node.left)):
                return firstpos(node.left) | firstpos(node.right)
            else:
                return firstpos(node.left)
        elif (node.value == "|"):
            return firstpos(node.left) | firstpos(node.right)



def lastpos(node):
    """
    Calculates the lastpos set for a given node in a syntax tree.

    Args:
        node (Node): The node for which to calculate the lastpos set.

    Returns:
        set: The lastpos set for the given node.
    """
    if (type(node) != Node):
        return set()

    # Base case, 1 node.
    if ((node.left == None) and (node.right == None)):
        if (node.value == "ε"):
            return set()
        else:
            return { node }

    # Inductive case, 2 nodes.
    else:
        if (node.value == "*"):
            return lastpos(node.left)
        elif (node.value == "+"):
            return lastpos(node.left)
        elif (node.value == "?"):
            return lastpos(node.left)
        elif (node.value == "."):
            if (nullable(node.right)):
                return lastpos(node.left) | lastpos(node.right)
            else:
                return lastpos(node.right)
        elif (node.value == "|"):
            return lastpos(node.left) | lastpos(node.right)


def followpos(node):
    """
    Calculates the followpos set for a given node in a syntax tree.

    Args:
        node (Node): The node for which to calculate the followpos set.

    Returns:
        set: The followpos set for the given node.
    """
    if (type(node) != Node):
        return set()

    # Base case, 1 node.
    if ((node.left == None) and (node.right == None)):
        return set()

    # Inductive case, 2 nodes.
    else:
        if ((node.value == "*") or (node.value == "+")):
            first_step = lastpos(node)
            for state in first_step:
                state.properties["followpos"] |= firstpos(node)
        elif (node.value == "."):
            first_step = lastpos(node.left)
            for state in first_step:
                state.properties["followpos"] |= firstpos(node.right)
        else:
            return set()



def dfa_direct_construction(postfix, tokens):
    """
    Constructs a DFA (Deterministic Finite Automaton) using the direct construction method.

    Args:
        postfix (str): The postfix expression representing the regular expression.
        tokens (list): A list of tokens associated with the regular expression.

    Returns:
        DFA: The constructed DFA object.
    """
    # Get the root node of the syntax tree and an array of nodes.
    expression_tree_root, node_array = build_syntax_tree(postfix)

    # Calculate the nullable, firstpos, lastpos, and followpos sets for each node in the syntax tree.
    for node in node_array:
        node.properties["nullable"] = nullable(node)
        node.properties["firstpos"] = firstpos(node)
        node.properties["lastpos"] = lastpos(node)
        node.properties["followpos"] = followpos(node)

    # DFA structure
    states = set()
    alphabet = set([char for char in postfix if char not in set(OPERATORS) | {"ε", "#"}])
    indexed_states = []
    mapping = {}
    state_stack = Stack()

    # Get the initial state
    initial_state = firstpos(expression_tree_root)
    state_stack.push(initial_state)
    indexed_states.append(initial_state)

    while (not state_stack.is_empty()):
        current_state = state_stack.pop()
        current_state_index = indexed_states.index(current_state)
        mapping[current_state_index] = {}

        for char in alphabet:
            next_state = set()

            for node in current_state:
                if (node.value == char):
                    next_state |= node.properties["followpos"]

            if (next_state not in indexed_states):
                indexed_states.append(next_state)
                state_stack.push(next_state)

            mapping[current_state_index][char] = indexed_states.index(next_state)

    # DFA State space
    for index in range(len(indexed_states)):
        states.add(index)

    # Initial state of the DFA
    initial_state = indexed_states.index(initial_state)

    # Acceptance states of the DFA
    acceptance_states = set([indexed_states.index(state) for state in indexed_states if (state & lastpos(expression_tree_root) != set())])
    acceptance_states = acceptance_states if (len(acceptance_states) > 0) else { initial_state }

    dead_states = set()

    states_copy = states.copy()

    # Dead state localization
    for dead_state in states_copy:
        if (all([mapping[dead_state][char] == dead_state for char in alphabet]) and (dead_state not in acceptance_states)):
            dead_states.add(dead_state)
            states.remove(dead_state)

    # Elimination of dead states from the DFA mapping
    for dead_state in dead_states:
        for state in states:
            for char in alphabet:
                entry_mapping = mapping.get(state, {})
                result = entry_mapping.get(char, False)
                if ((type(result) != bool) and (mapping[state][char] == dead_state)):
                    del mapping[state][char]
        del mapping[dead_state]

    if (len(mapping) < 2):
        states = { 0 }
        mapping = { 0: { char: 0 for char in alphabet } }

    # Add acceptance states to the DFA
    for state in states:
        for index in range(len(tokens)):
            if (f"#{index}" in mapping[state]):
                acceptance_states.add((state, tokens[index]))

    # Eliminación de los estados de aceptación y sus tokens del conjunto de estados
    acceptance_states_copy = acceptance_states.copy()

    # Elimination of acceptance states that are not tuples
    for state in acceptance_states_copy:
        if (type(state) != tuple):
            acceptance_states.remove(state)

    # Return the constructed DFA
    return DFA(
        states=states,
        alphabet=alphabet,
        initial_state=initial_state,
        acceptance_states=acceptance_states,
        mapping=mapping
    )
