import sys

sys.path.insert(0, '../tkml')

from tkml.lex import lex
from tkml.parse import parser

def assert_equal(string, expected_tree):
    parsed_tree = parser.parse(string)
    print(parsed_tree)
    return
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

assert_equal('()', [])
assert_equal('((@x))', [])
assert_equal('((@x) (@y) (@z))', [])
assert_equal('((@x (grid-kwarg a "b")))', [])
assert_equal('((@x (grid-kwarg a "b") (grid-kwarg c "d")))', [])
assert_equal('((@x (grid-kwarg a 2)))', [])
assert_equal('((Button))', [])

'''
print(parser.parse('(root (defs) (body))'))
print(parser.parse('(root (defs (@x)) (body))'))
print(parser.parse('(root (defs (@x) (@y) (@z)) (body))'))
print(parser.parse('(root (defs (@x)) (body))'))
print(parser.parse('(root (defs (@x (rows "+"))) (body))'))
print(parser.parse('(root (defs (@x (rows "+") (rows "-"))) (body))'))
#print(parser.parse('(root (defs))'))
#print(parser.parse('(root (body))'))
#print(parser.parse('(root)'))
print(parser.parse('(root (defs) (body (div)))'))
print(parser.parse('(root (defs (@x) (@y) (@z)) (body (div) (div) (div)))'))
print(parser.parse('(root (defs) (body (div (div))))'))
print(parser.parse('(root (defs) (body (div #test)))'))
print(parser.parse('(root (defs) (body (div #test (div))))'))
print(parser.parse('(root (defs) (body (div #test (div #test2))))'))
print(parser.parse('(root (defs) (body (div @test)))'))
print(parser.parse('(root (defs) (body (div @test (div))))'))
print(parser.parse('(root (defs) (body (div) @test (div)))'))
print(parser.parse('(root (defs) (body (div @test @test (div))))'))
print(parser.parse('(root (defs) (body (div @test (div @test2))))'))
print(parser.parse('(root (defs) (body @test))'))
print(parser.parse('(root (defs) (body (label "test")))'))
print(parser.parse('(root (defs) (body (label @test "test")))'))
print(parser.parse('(root (defs) (body (div (label "test"))))'))
'''

#with open('./examples/ultratrace.tkml') as fp:
#    for line in fp:
#        for token in lex(line):
#            pass

print('all tests passed!')
