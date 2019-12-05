import sys

sys.path.insert(0, '../tkml')

from tkml.lex import lex
from tkml.parse import *

NotReached = False

def assert_throws(string, Error):
    try:
        parser.parse(string)
        assert NotReached
    except Error as e:
        pass

def assert_equal(string, expected_tree):
    def assert_equal_dfs(parsed_node, expected_node):
        assert type(parsed_node) == type(expected_node)\
                , f'Expected {type(expected_node)}, got {type(parsed_node)}'
        if not isinstance(parsed_node, ParseNode):
            return
        assert len(parsed_node) == len(expected_node)\
                , f'Expected {len(expected_node)} children, got {len(parsed_node)}'
        for parsed_child, expected_child in zip(parsed_node, expected_node):
            assert_equal_dfs(parsed_child, expected_child)

    try:
        parsed_tree = parser.parse(string)
        assert_equal_dfs(parsed_tree, expected_tree)
    except ParseError as e:
        print(f'Error while parsing "{string}":\n\t{e}')
        exit()
    except AssertionError as e:
        print(f'Error while parsing "{string}" (expected "{expected_tree}", got "{parsed_tree}"):\n\t{e}')
        exit()

assert_throws('(', EOFError)
assert_throws('', EOFError)
assert_throws(':def', ParseError)
assert_throws('(:def)', ParseError)
assert_throws('(x)', ParseError)
assert_equal('()',
        RootNode())
assert_equal('(())',
        RootNode(ParseNode()))
assert_equal('((:def @x))',
        RootNode(ParseNode(IncludeDefNode('x'))))
assert_equal('(((:def @x)))',
        RootNode(ParseNode(ParseNode(IncludeDefNode('x')))))
assert_equal('((:def @x) (:def @y) (:def @z))',
        RootNode(
            ParseNode(IncludeDefNode('x')),
            ParseNode(IncludeDefNode('y')),
            ParseNode(IncludeDefNode('z'))))
assert_equal('((:def @x (grid-kwarg a "b")))',
        RootNode(
            ParseNode(IncludeDefNode('x'),
                ParseNode(ParseNode(
                    BareNode('grid-kwarg'),
                    BareNode('a'),
                    StrLiteral('b'))))))
assert_equal('((:def @x (grid-kwarg a "b") (grid-kwarg c "d")))',
        RootNode(
            ParseNode(IncludeDefNode('x'),
                ParseNode(ParseNode(
                    BareNode('grid-kwarg'),
                    BareNode('a'),
                    StrLiteral('b'))),
                ParseNode(ParseNode(
                    BareNode('grid-kwarg'),
                    BareNode('c'),
                    StrLiteral('d'))))))
assert_equal('((:def @x (grid-kwarg a 2)))',
        RootNode(
            ParseNode(IncludeDefNode('x'),
                ParseNode(ParseNode(
                    BareNode('grid-kwarg'),
                    BareNode('a'),
                    IntLiteral(2))))))
assert_equal('((Button))',
        RootNode(ParseNode(WidgetNode('Button'))))
assert_equal('(((Button)))',
        RootNode(ParseNode(ParseNode(WidgetNode('Button')))))
assert_equal('(Button)',
        RootNode(WidgetNode('Button')))
assert_equal('((Button) (:def @x))', # should throw (eventually)
        RootNode(ParseNode(WidgetNode('Button')), ParseNode(IncludeDefNode('x'))))
assert_equal('((Button @x))',
        RootNode(ParseNode(WidgetNode('Button'), IncludeNode('x'))))
assert_equal('((Button #x))',
        RootNode(ParseNode(WidgetNode('Button'), IdNode('x'))))
assert_equal('((Button #x @x))',
        RootNode(ParseNode(WidgetNode('Button'), IdNode('x'), IncludeNode('x'))))
assert_equal('((Button @x #x))',
        RootNode(ParseNode(WidgetNode('Button'), IncludeNode('x'), IdNode('x'))))
assert_equal('((Button #x #y))', # allow multiple id's ?
        RootNode(ParseNode(WidgetNode('Button'), IdNode('x'), IdNode('y'))))
assert_equal('((#x))',
        RootNode(ParseNode(IdNode('x'))))
assert_equal('(Button $x)',
        RootNode(WidgetNode('Button'), VarNode('x')))
assert_equal('(Button "x")',
        RootNode(WidgetNode('Button'), StrLiteral('x')))
assert_equal('(Button 69)',
        RootNode(WidgetNode('Button'), IntLiteral(69)))

with open('./examples/ultratrace.tkml') as fp:
    parser.parse(fp.read())

#print('all tests passed!')
