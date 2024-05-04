class Node():
    """
    Represents a node in a binary tree.

    Attributes:
        value: The value stored in the node.
        position: The position of the node.
        left: The left child of the node.
        right: The right child of the node.
        properties: A dictionary containing properties of the node.
    """

    def __init__(self, value, position=None):
        self.value = value
        self.position = position
        self.left = None
        self.right = None
        self.properties = {"firstpos": set(), "lastpos": set(), "followpos": set()}

    def __repr__(self):
        str_repr = "Node(\n"
        str_repr += f"\tvalue={self.value},\n"
        str_repr += f"\tleft={self.left},\n"
        str_repr += f"\tright={self.right},\n"
        str_repr += f"\tproperties={self.properties}\n"
        str_repr += ")"
        return str_repr