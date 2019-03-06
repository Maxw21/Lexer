'''
Assignment 1 - Lexical Analyzer
CPSC 323 Spring 2019
Maxfield Wilhoite
'''

from lexer import Lexer

while True:
    try:
        source_file = open(input("Enter name of file with file extension to be analyzed by lexer: "), 'r')
    except IOError:
        print("Error opening file")
    else:
        print("File successfully opened.")
        break

lexer = Lexer(source_file=source_file)
lexer.analyze()
lexer.results()
