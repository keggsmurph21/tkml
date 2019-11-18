import ply.yacc as yacc
from .tokens import tokens

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

def p_root(p):
    '''
    root        : LPAREN abstractnodes RPAREN
    '''
    p[0] = Node(*p[2])

def p_abstractnodes(p):
    '''
    abstractnodes   : abstractnode abstractnodes
                    | empty
    '''
    if len(p) == 3:
        p[0] = Node(p[1], *p[2])
    else:
        p[0] = []

def p_abstractnode(p):
    '''
    abstractnode    : include
                    | widget
    '''
    p[0] = p[1]

def p_includes(p):
    '''
    includes    : include includes
                | empty
    '''
    if len(p) == 3:
        p[0] = Node(p[1], *p[2])
    else:
        p[0] = []

def p_include(p):
    '''
    include      : LPAREN INCLUDEIDENTIFIER includeargs RPAREN
    '''
    p[0] = Node(p[2], *p[3])

def p_includeargs(p):
    '''
    includeargs : includearg includeargs
                | empty
    '''
    if len(p) == 3:
        p[0] = Node(p[1], *p[2])
    else:
        p[0] = []

def p_includearg(p):
    '''
    includearg  : LPAREN BAREIDENTIFIER BAREIDENTIFIER STRLITERAL RPAREN
                | LPAREN BAREIDENTIFIER BAREIDENTIFIER INTLITERAL RPAREN
    '''
    p[0] = Node(p[2], p[3], p[4])

def p_widgets(p):
    '''
    widgets     : widget widgets
                | empty
    '''
    if len(p) == 3:
        p[0] = Node(p[1], *p[2])
    else:
        p[0] = []

def p_widget(p):
    '''
    widget      : LPAREN WIDGETIDENTIFIER widgetargs RPAREN
    '''
    print(p)
    p[0] = Node(p[2], *p[3])

def p_widgetargs(p):
    '''
    widgetargs  : empty
    '''
    if len(p) == 3:
        p[0] = Node(p[1], *p[2])
    else:
        p[0] = []

def p_empty(p):
    '''
    empty       :
    '''

def p_error(p):
    raise ValueError(f'Parse error in input: {p}')

parser = yacc.yacc()
