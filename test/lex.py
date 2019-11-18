import sys

sys.path.insert(0, '../tkml')

from tkml.lex import lex

def assert_equal(string, expected_tokens):
    lexed_tokens = lex(string)
    for i, (lexed_token, expected_token) in enumerate(zip(lexed_tokens, expected_tokens)):
        try:
            if isinstance(expected_token, tuple):
                expected_type, expected_value = expected_token
                assert lexed_token.type == expected_type\
                        , f'Expected type "{expected_type}", got "{lexed_token.type}"'
                assert lexed_token.value == expected_value\
                        , f'Expected value "{expected_value}", got "{lexed_token.value}"'
            else:
                expected_type = expected_token
                assert lexed_token.type == expected_type\
                        , f'Expected type "{expected_type}", got "{lexed_token.type}"'
        except AssertionError as e:
            print(f'Error while lexing "{string}" at token {i}:\n\t{e}')
            exit()

assert_equal('', [])
assert_equal('()', ['LPAREN', 'RPAREN'])
assert_equal('(* hello *)', ['LPAREN', 'RPAREN'])
assert_equal('(hello)', ['LPAREN', ('BAREIDENTIFIER', 'hello'), 'RPAREN'])
assert_equal('(@hello)', ['LPAREN', ('INCLUDEIDENTIFIER', 'hello'), 'RPAREN'])
assert_equal('(#hello)', ['LPAREN', ('IDIDENTIFIER', 'hello'), 'RPAREN'])
assert_equal('($hello)', ['LPAREN', ('VARIDENTIFIER', 'hello'), 'RPAREN'])
assert_equal('(Hello)', ['LPAREN', ('WIDGETIDENTIFIER', 'Hello'), 'RPAREN'])
assert_equal('("hello")', ['LPAREN', ('STRLITERAL', 'hello'), 'RPAREN'])
assert_equal('(1)', ['LPAREN', 'INTLITERAL', 'RPAREN'])

with open('./examples/ultratrace.tkml') as fp:
    for line in fp:
        for token in lex(line):
            pass

print('all tests passed!')
