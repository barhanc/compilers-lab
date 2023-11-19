import sys
import sly.yacc as yacc
from mparser import MyParser
from scanner import MyLexer
from TreePrinter import TreePrinter


if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = MyLexer()
    parser = MyParser()

    text = file.read()
    tokens = lexer.tokenize(text=text)

    for a in parser.parse(tokens):
        a.printTree()
