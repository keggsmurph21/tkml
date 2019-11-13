from .lex import lex
from .parse import parser

while True:
    try:
        chars = input('tkml> ')
    except EOFError:
        break
    if not chars:
        continue
    print(parser.parse(chars))
