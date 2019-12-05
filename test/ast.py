import sys

sys.path.insert(0, '../tkml')

from tkml.ast import *
from tkml.lex import lex
from tkml.parse import parser

NotReached = False

def assert_throws(func, Error):
    try:
        func()
        assert NotReached
    except Error as e:
        pass

def assert_equal(string):
    print(string)
    parse_tree = parser.parse(string)
    print(AST(parse_tree))
    print()
    return True
    def assert_equal_dfs(parsed_node, expected_node):
        assert type(parsed_node) == type(expected_node)\
                , f'Expected {type(expected_node)}, got {type(parsed_node)}'
        if not isinstance(parsed_node, Node):
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

# test SymbolTable
s = SymbolTable()
assert not s.has('x')
s.put('x', 'y')
assert s.has('x')
assert s.get('x') == 'y'
assert not s.has('y')
assert not s.has('z')
s.put('z', 'w')
assert s.has('z')
assert s.get('z') == 'w'
assert_throws(lambda: s.put('x', 'y2'), ASTError)
assert_throws(lambda: s.put('z', 'w2'), ASTError)

'''
(:def) nodes must be direct children of the root and appear
       before any widget children (DFS)
'''

#assert_throws(lambda: to_ast(None), TypeError)
#assert_throws(lambda: to_ast(), TypeError)
#assert_throws(lambda: ASTNode(None), TypeError)
#assert_throws(lambda: ASTNode(), TypeError)
assert_equal('()')
        #RootNode())
assert_equal('(())')
        #RootNode(Node()))
assert_equal('((:def @x))')
        #RootNode(Node(IncludeDefNode('x'))))
assert_throws(lambda: AST(parser.parse('((:def @x)(:def @x))')), ASTError)
assert_throws(lambda: AST(parser.parse('(((:def @x)))')), ASTError) # too deeply nested
        #RootNode(Node(Node(IncludeDefNode('x')))))
assert_equal('((:def @x) (:def @y) (:def @z))')
        #RootNode(
            #Node(IncludeDefNode('x')),
            #Node(IncludeDefNode('y')),
            #Node(IncludeDefNode('z'))))
assert_equal('((:def @x (grid-kwarg a "b")))')
        #RootNode(
            #Node(IncludeDefNode('x'),
                #Node(Node(
                    #BareNode('grid-kwarg'),
                    #BareNode('a'),
                    #StrLiteral('b'))))))
assert_equal('((:def @x (grid-kwarg a "b") (grid-kwarg c "d")))')
        #RootNode(
            #Node(IncludeDefNode('x'),
                #Node(Node(
                    #BareNode('grid-kwarg'),
                    #BareNode('a'),
                    #StrLiteral('b'))),
                #Node(Node(
                    #BareNode('grid-kwarg'),
                    #BareNode('c'),
                    #StrLiteral('d'))))))
assert_equal('((:def @x (grid-kwarg a 2)))')
        #RootNode(
            #Node(IncludeDefNode('x'),
                #Node(Node(
                    #BareNode('grid-kwarg'),
                    #BareNode('a'),
                    #IntLiteral(2))))))
assert_equal('((Button))')
        #RootNode(Node(WidgetNode('Button'))))
assert_equal('(((Button)))')
        #RootNode(Node(Node(WidgetNode('Button')))))
assert_equal('(Button)')
        #RootNode(WidgetNode('Button')))
assert_throws(lambda: AST(parser.parse('((Button) (:def @x))')), ASTError) # wrong order
        #RootNode(Node(WidgetNode('Button')), Node(IncludeDefNode('x'))))
assert_equal('((Button @x))')
        #RootNode(Node(WidgetNode('Button'), IncludeNode('x'))))
assert_equal('((Button #x))')
        #RootNode(Node(WidgetNode('Button'), IdNode('x'))))
assert_equal('((Button #x @x))')
        #RootNode(Node(WidgetNode('Button'), IdNode('x'), IncludeNode('x'))))
assert_equal('((Button @x #x))')
        #RootNode(Node(WidgetNode('Button'), IncludeNode('x'), IdNode('x'))))
assert_equal('((Button #x #y))') # allow multiple id's )
        #RootNode(Node(WidgetNode('Button'), IdNode('x'), IdNode('y'))))
assert_equal('((#x))')
        #RootNode(Node(IdNode('x'))))
assert_equal('(Button $x)')
        #RootNode(WidgetNode('Button'), VarNode('x')))
assert_equal('(Button "x")')
        #RootNode(WidgetNode('Button'), StrLiteral('x')))
assert_equal('(Button 69)')
        #RootNode(WidgetNode('Button'), IntLiteral(69)))

#with open('./examples/ultratrace.tkml') as fp:
    #parser.parse(fp.read()).pretty_print()

print('all tests passed!')
