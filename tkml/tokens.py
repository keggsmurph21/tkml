tokens = (
    'COMMENT',
    'INTLITERAL',
    'STRLITERAL',
    'LPAREN',
    'RPAREN',
    'VAR',
    'ROOT',
    'DEFS',
    'BODY',
    'ID',
    'INCLUDE',
    'DIV',
    'ICON',
    'LABEL',
    'BUTTON',
    'DROPDOWN',
    'INPUT',
    'LISTBOX',
    'CANVAS',
    'IDENTIFIER')

def t_COMMENT(t):
    r'\(\*.*?\*\)'
    pass

def t_INTLITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRLITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_VAR(t):
    'var'
    return t

def t_ROOT(t):
    'root'
    return t

def t_DEFS(t):
    'defs'
    return t

def t_BODY(t):
    'body'
    return t

def t_ID(t):
    r'\#'
    return t

def t_INCLUDE(t):
    r'\@'
    return t

def t_DIV(t):
    'div'
    return t

def t_ICON(t):
    'icon'
    return t

def t_LABEL(t):
    'label'
    return t

def t_BUTTON(t):
    'button'
    return t

def t_DROPDOWN(t):
    'dropdown'
    return t

def t_INPUT(t):
    'input'
    return t

def t_LISTBOX(t):
    'listbox'
    return t

def t_CANVAS(t):
    'canvas'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][\w-]*'
    return t

t_ignore    = ' \t\n'

class LexError(Exception):
    def __init__(self, t):
        super().__init__(f'Illegal character "{t.value[0]}" at position {t.lexpos}')

def t_error(t):
    raise LexError(t)

