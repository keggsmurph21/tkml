tokens = (
    'COMMENT',
    'INTLITERAL',
    'STRLITERAL',
    'LPAREN',
    'RPAREN',
    'DEF',
    'SET',
    'VARIDENTIFIER',
    'IDIDENTIFIER',
    'INCLUDEIDENTIFIER',
    'WIDGETIDENTIFIER',
    'BAREIDENTIFIER')


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

def t_DEF(t):
    r':def'
    t.value = 'def'
    return t

def t_SET(t):
    r':set'
    t.value = 'set'
    return t

def t_VARIDENTIFIER(t):
    r'\$[a-zA-Z][\w-]*'
    t.value = t.value[1:]
    return t

def t_IDIDENTIFIER(t):
    r'\#[a-zA-Z][\w-]*'
    t.value = t.value[1:]
    return t

def t_INCLUDEIDENTIFIER(t):
    r'\@[a-zA-Z][\w-]*'
    t.value = t.value[1:]
    return t

def t_WIDGETIDENTIFIER(t):
    r'[A-Z][\w-]*'
    return t

def t_BAREIDENTIFIER(t):
    r'[a-z][\w-]*'
    return t

t_ignore    = ' \t\n'

class LexError(Exception):
    def __init__(self, t):
        super().__init__(f'Illegal character "{t.value[0]}" at position {t.lexpos}')

def t_error(t):
    raise LexError(t)

