class Stack():
    """
    A class representing a stack data structure.

    Attributes:
        stack (list): The list that holds the elements of the stack.

    Methods:
        __init__(self, initial_values=[]): Initializes a new instance of the Stack class.
        __len__(self): Returns the number of elements in the stack.
        __contains__(self, item): Returns True if the item is in the stack, False otherwise.
        __repr__(self): Returns a string representation of the stack.
        is_empty(self): Returns True if the stack is empty, False otherwise.
        push(self, item): Adds an item to the top of the stack.
        peek(self): Returns the top element of the stack without removing it.
        pop(self): Removes and returns the top element of the stack.
    """

    def __init__(self, initial_values=[]):
        self.stack = initial_values

    def __len__(self):
        return len(self.stack)

    def __contains__(self, item):
        return (item in self.stack)

    def __repr__(self):
        return str(self.stack)

    def is_empty(self):
        return (len(self.stack) == 0)

    def push(self, item):
        self.stack.append(item)

    def peek(self):
        return (self.stack[-1] if (not self.is_empty()) else "")

    def pop(self):
        last_element = (self.stack[-1] if (not self.is_empty()) else "")
        try:
            self.stack.pop(-1)
        except:
            pass
        return last_element