from .lex import lex, LexError
from .parse import parser, ParseError

while True:
    try:
        chars = input('tkml> ')
    except EOFError:
        break
    if not chars:
        continue
    try:
        print(parser.parse(chars))
    except (LexError, ParseError) as e:
        print(e)
