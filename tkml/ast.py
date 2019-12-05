from . import parse as p

class ASTError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.table = {}
    def has(self, key):
        return key in self.table
    def get(self, key):
        if not self.has(key):
            raise ASTError(f'Cannot find key {key}')
        return self.table[key]
    def put(self, key, value):
        if self.has(key):
            raise ASTError(f'Cannot have multiple values for key {key}')
        self.table[key] = value
    def __len__(self):
        return len(self.table)
    def __repr__(self):
        return f'SymbolTable({repr(self.table)})'

def tree_contains(tree, NodeType, level=0):
    if isinstance(tree, NodeType):
        return True
    for child in tree:
        if tree_contains(child, NodeType, level + 1):
            return True
    return False

def is_leaf(node):
    return len(node) == 0

def extract_include_def(tree):
    if not len(tree):
        raise ASTError()
    def_node, *def_children = tree
    if not isinstance(def_node, p.IncludeDefNode):
        raise ASTError()
    if len(def_children) == 0:
        return def_node.value, None
    include_node = ASTNode()
    for def_child in def_children:
        if len(def_child) != 1:
            raise ASTError()
        include_node.add_child(cast(def_child[0], (ArgumentNode,)))
    return def_node.value, include_node

class AST:
    def __init__(self, parse_tree):
        if not isinstance(parse_tree, p.RootNode):
            raise ASTError(f'Cannot construct AST from instance of {type(parse_tree).__name__}')
        self.ids = SymbolTable()
        self.vars = SymbolTable()
        self.includes = SymbolTable()

        has_seen_widgets = False

        for child in parse_tree:
            if tree_contains(child, p.IncludeDefNode):
                if has_seen_widgets:
                    raise ASTError()
                self.includes.put(*extract_include_def(child))
            else:
                WidgetNode(child)
                has_seen_widgets = True

    def __repr__(self):
        string = 'AST('
        tables = [ f'{name}={getattr(self, name)}' for name in ['ids', 'vars', 'includes']
                        if len(getattr(self, name)) ]
        string += ','.join(tables)
        string += ')'
        return string


class ASTNode:
    def __init__(self):#, parse_node):
        self.children = []
        self.parent = None
        #for child in parse_node.children:
            #print(child)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def clone(self):
        raise NotImplementedError()

    def __repr__(self):
        string = f'({type(self).__name__}'
        if len(self.children):
            string += ' '
            string += ' '.join(map(repr, self.children))
        string += ')'
        return string

class WidgetNode(ASTNode):
    def __init__(self, node):
        super().__init__()
        self.id = None
        self.var = None
        print(node)

class ArgumentNode(ASTNode):
    #child_types = [p.BareNode, p.BareNode, (p.StrLiteral, p.IntLiteral)]
    def __init__(self, parse_node):
        if len(parse_node) != 3:
            raise ASTError()
        if not isinstance(parse_node[0], p.BareNode):
            raise ASTError()
        if not isinstance(parse_node[1], p.BareNode):
            raise ASTError()
        if not isinstance(parse_node[2], (p.StrLiteral, p.IntLiteral)):
            raise ASTError()

        self.argtype = parse_node[0].value
        self.argkey  = parse_node[1].value
        self.argval  = parse_node[2].value

        #if len(parse_node) != len(self.child_types):
            #raise ASTError(f'ArgumentNode: invalid len '
                    #f'(expecting {len(self.child_types)}, got {len(parse_node)}')
        #for child, child_type in zip(parse_node, self.child_types):
            #if isinstance(child_type, tuple):
                #for possible_child_type in child_type
        #if not isinstance(parse_node[0], p.BareNode):
            #raise ASTError(f'ArgumentNode: invalid argtype (expecting BareNode, got {
                #or not isinstance(parse_

    def __repr__(self):
        return f'ArgumentNode({self.argtype},{self.argkey},{self.argval})'

def cast(tree, node_types):
    for NodeType in node_types:
        try:
            return NodeType(tree)
        except ASTError:
            pass
    raise ASTError()

def to_ast(parse_tree):
    if not isinstance(parse_tree, p.RootNode):
        raise TypeError(f'Cannot construct AST from instance of {type(parse_tree).__name__}')
    return ASTNode(parse_tree)
