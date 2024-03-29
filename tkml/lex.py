from ply.lex import lex as ply_lex
from . import tokens
from .tokens import LexError

lexer = ply_lex(module=tokens)

def lex(chars):
    lexer.input(chars)
    for token in lexer:
        yield token
