from . import parse as p

class ASTNode:
    def __init__(self, parse_node):
        self.children = []
        self.parent = None
        for child in parse_node.children:
            print(child)

    def add_child(self, child):
        # do some checking
        if not isinstance(parse_node, p.ParseNode):
            raise TypeError(f'Cannot add_child of type {type(parse_node).__name__}')

def to_ast(parse_tree):
    if not isinstance(parse_tree, p.RootNode):
        raise TypeError(f'Cannot construct AST from instance of {type(parse_tree).__name__}')
    return ASTNode(parse_tree)
