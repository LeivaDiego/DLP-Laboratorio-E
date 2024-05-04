import graphviz

def show_node(node, visual_tree):
    """
    Recursively displays a binary tree node and its children in a visual tree.

    Args:
        node: The current node to display.
        visual_tree: The visual tree object to add the node and edges to.

    Returns:
        None
    """
    if (node is not None):
        label = str(node.value) if ((node.left != None) or (node.right != None) or (node.value.startswith("#"))) else str(chr(int(node.value)))
        visual_tree.node(str(id(node)), label, shape="circle")
        if (node.left != None):
            visual_tree.edge(str(id(node)), str(id(node.left)))
            show_node(node.left, visual_tree)
        if (node.right != None):
            visual_tree.edge(str(id(node)), str(id(node.right)))
            show_node(node.right, visual_tree)


def display_syntax_tree(root, view=True, name=""):
    """
    Renders and displays an expression tree using graphviz.

    Args:
        root: The root node of the expression tree.
        view (bool): Whether to open the rendered image after saving. Defaults to True.
        name (str): The name of the output file. Defaults to an empty string.

    Returns:
        None
    """
    visual_tree = graphviz.Digraph(comment="Expression Tree")
    show_node(root, visual_tree)
    visual_tree.render(f"./out/mega_tree_{name}", format="png", view=view, cleanup=True)
