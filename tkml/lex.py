from ply.lex import lex
from . import tokens

lexer = lex(module=tokens)

def lex(chars):
    lexer.input(chars)
    for token in lexer:
        yield token
