import sys

sys.path.insert(0, '../tkml')

from tkml.lex import lex
from tkml.parse import parser

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
#print(parser.parse('(root (defs) (body (button "test"k
