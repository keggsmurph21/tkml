import sys

sys.path.insert(0, '../tkml')

from tkml.lex import lex

#print(list(lex('hello world')))
#print(list(lex('hello "world"')))
#print(list(lex('hello (world)')))
#print(list(lex('hello (# world #)')))
#print(list(lex('hello (# #) #)')))

with open('./examples/ultratrace.tkml') as fp:
    for line in fp:
        for token in lex(line):
            print(token)

#print(list(lex('hello "news"')))
#print(list(lex('hello "NnNnEe"')))
