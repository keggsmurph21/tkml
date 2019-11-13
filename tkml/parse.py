import ply.yacc as yacc
from .tokens import tokens

'''
class SymbolTable:
    def __init__(self):
        self.symbols = dict()
    def put(self, key, val):
        if key in self.symbols:
            raise KeyError(f'key "{key}" already exists in table')
        self.symbols[key]
    def get(self, key):
        return self.symbols.get(key, None)
    def has(self, key):
        return self.get(key) is None
    def clear(self):
        self.symbols = dict()
'''

class Node:
    def __init__(self, *children):
        self.children = children
    def __iter__(self):
        for child in self.children:
            yield child
    def __len__(self):
        return len(self.children)
    def __repr__(self):
        string = f'({type(self).__name__}'
        if hasattr(self, 'name'):
            if self.name is not None:
                string += ' ' + repr(self.name)
        if len(self):
            string += ' '
            string += ' '.join(map(repr, self))
        string += ')'
        return string

class Root(Node):       pass
class Defs(Node):       pass
class Def(Node):
    def __init__(self, name, *children):
        super().__init__(*children)
        self.name = name
class Attr(Node):       pass
class Rows(Node):       pass
class Row(Node):        pass
class Cols(Node):       pass
class Col(Node):        pass
class Sticky(Node):     pass
class Body(Node):       pass
class Label(Node):      pass
class Id(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name
class Include(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

class IdentifiableNode(Node):
    def __init__(self, name, *children):
        super().__init__(*children)
        self.name = name

class Div(IdentifiableNode):        pass
class Text(IdentifiableNode):       pass
class Icon(IdentifiableNode):       pass
class Button(IdentifiableNode):     pass
class Dropdown(IdentifiableNode):   pass
class Input(IdentifiableNode):      pass
class Listbox(IdentifiableNode):    pass
class Canvas(IdentifiableNode):     pass

def p_root(p):
    '''
    root        : LPAREN ROOT defs body RPAREN
    '''
    p[0] = Root(p[3], p[4])

def p_defs(p):
    '''
    defs        : LPAREN DEFS defnode RPAREN
    '''
    p[0] = Defs(*p[3])

def p_defnode(p):
    '''
    defnode     : def defnode
                | empty
    '''
    if len(p) == 3:
        p[0] = [p[1], *p[2]]
    else:
        p[0] = []

def p_def(p):
    '''
    def         : LPAREN INCLUDE IDENTIFIER attrnode RPAREN
    '''
    p[0] = Def(p[3], *p[4])

def p_attrnode(p):
    '''
    attrnode    : attr attrnode
                | empty
    '''
    if len(p) == 3:
        p[0] = [p[1], *p[2]]
    else:
        p[0] = []

def p_attr(p):
    '''
    attr        : LPAREN IDENTIFIER STRLITERAL RPAREN
    '''
    p[0] = Attr(p[2], p[3])

def p_body(p):
    '''
    body        : LPAREN BODY divnode RPAREN
    '''
    p[0] = Body(*p[3])

def p_divnode(p):
    '''
    divnode     : empty
    '''
    p[0] = []

def p_include_divnode(p):
    '''
    divnode     : include divnode
    '''
    p[0] = [p[1], *p[2]]

def p_div_divnode(p):
    '''
    divnode     : div divnode
    '''
    p[0] = [p[1], *p[2]]

def p_div(p):
    '''
    div         : LPAREN DIV id includes divnode RPAREN
    '''
    p[0] = Div(p[3], *p[4], *p[5])

def p_label_divnode(p):
    '''
    divnode     : label divnode
    '''
    p[0] = [p[1], *p[2]]

def p_label(p):
    '''
    label       : LPAREN LABEL includes STRLITERAL RPAREN
    '''
    p[0] = Label(*p[3], p[4])

def p_includes(p):
    '''
    includes     : include includes
                 | empty
    '''
    if len(p) == 3:
        p[0] = [p[1], *p[2]]
    else:
        p[0] = []

def p_include(p):
    '''
    include     : INCLUDE IDENTIFIER
    '''
    p[0] = Include(p[2])

def p_id(p):
    '''
    id          : ID IDENTIFIER
                | empty
    '''
    if len(p) == 3:
        p[0] = Id(p[2])
    else:
        p[0] = None

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    raise ValueError(f'Parse error in input: {p}')

parser = yacc.yacc()

# these can be during AST construction
#parser.ids = SymbolTable()
#parser.classes = SymbolTable()
#parser.vars = SymbolTable()
'''
id          : ( ID STRLITERAL )
            | empty
class       : ( CLASS STRLITERAL ) class
            | empty

div         : ( DIV id class divnode )
divnode     : text divnode
            | icon divnode
            | label divnode
            | button divnode
            | dropdown divnode
            | input divnode
            | listbox divnode
            | canvas divnode
            | empty

text        : ( TEXT STRLITERAL )
icon        : ( ICON STRLITERAL )
label       : ( LABEL id class text )
button      : ( BUTTON id class text )
            | ( BUTTON id class icon )
dropdown    : ( DROPDOWN id class var )
input       : ( INPUT id class var )
listbox     : ( LISTBOX id class )
canvas      : ( CANVAS id class )

var         : ( VAR varid )

empty       :
'''

