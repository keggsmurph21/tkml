import ply.yacc as yacc
from .tokens import tokens

class ParseError(Exception):
    def __init__(self, t):
        super().__init__(f'Unexpected {t.type} ("{t.value}") at position {t.lexpos}')

class ParseNode:
    def __init__(self, *children):
        self.children = children
    def __iter__(self):
        for child in self.children:
            yield child
    def __getitem__(self, index):
        return self.children[index]
    def __len__(self):
        return len(self.children)
    def __repr__(self):
        string = f'({type(self).__name__}'
        if isinstance(self, ValueNode):
            string += ' ' + repr(self.value)
        if len(self):
            string += ' '
            string += ' '.join(map(repr, self))
        string += ')'
        return string
    def pretty_print(self, indent=0):
        print(f'{" "*(indent*4)}({type(self).__name__}', end='')
        if isinstance(self, ValueNode):
            print(' ', end='')
            print(repr(self.value), end='')
        for child in self:
            print()
            child.pretty_print(indent + 1)
        print(')', end='')

class RootNode(ParseNode): pass

class ValueNode(ParseNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

class BareNode(ValueNode): pass
class IncludeNode(ValueNode): pass
class IncludeDefNode(ValueNode): pass
class IdNode(ValueNode): pass
class VarNode(ValueNode): pass
class WidgetNode(ValueNode): pass
class StrLiteral(ValueNode):
    def __repr__(self):
        return f'"{self.value}"'
class IntLiteral(ValueNode):
    def __repr__(self):
        return f'{self.value}'


def p_start(p):
    '''
    start       : list
    '''
    p[0] = RootNode(*p[1])

def p_list(p):
    '''
    list        : LPAREN items RPAREN
    '''
    p[0] = ParseNode(*p[2])

def p_items_recursive(p):
    '''
    items       : item items
    '''
    p[0] = ParseNode(p[1], *p[2])

def p_items_empty(p):
    '''
    items       : empty
    '''
    p[0] = []

def p_item_list(p):
    '''
    item        : list
    '''
    p[0] = p[1]

def p_item_def_include(p):
    '''
    item        : DEF INCLUDEIDENTIFIER
    '''
    p[0] = IncludeDefNode(p[2])

def p_item_bare_bare_str(p):
    '''
    item        : BAREIDENTIFIER BAREIDENTIFIER STRLITERAL
    '''
    p[0] = ParseNode(BareNode(p[1]), BareNode(p[2]), StrLiteral(p[3]))

def p_item_bare_bare_int(p):
    '''
    item        : BAREIDENTIFIER BAREIDENTIFIER INTLITERAL
    '''
    p[0] = ParseNode(BareNode(p[1]), BareNode(p[2]), IntLiteral(p[3]))

def p_item_widget(p):
    '''
    item        : WIDGETIDENTIFIER
    '''
    p[0] = WidgetNode(p[1])

def p_item_include(p):
    '''
    item        : INCLUDEIDENTIFIER
    '''
    p[0] = IncludeNode(p[1])

def p_item_id(p):
    '''
    item        : IDIDENTIFIER
    '''
    p[0] = IdNode(p[1])

def p_item_var(p):
    '''
    item        : VARIDENTIFIER
    '''
    p[0] = VarNode(p[1])

def p_item_str(p):
    '''
    item        : STRLITERAL
    '''
    p[0] = StrLiteral(p[1])

def p_item_int(p):
    '''
    item        : INTLITERAL
    '''
    p[0] = IntLiteral(p[1])

def p_empty(p):
    '''
    empty       :
    '''

def p_error(t):
    if t is None:
        raise EOFError
    raise ParseError(t)

parser = yacc.yacc()
