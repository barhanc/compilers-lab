import sys
import sly.yacc as yacc

from scanner import MyLexer
from mparser import MyParser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker


if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = MyLexer()
    parser = MyParser()
    typeChecker = TypeChecker()

    text = file.read()
    tokens = lexer.tokenize(text=text)

    for a in parser.parse(tokens):
        a.printTree()
        try:
            typeChecker.visit(a)
        except Exception as e:
            # print(e)
            pass
