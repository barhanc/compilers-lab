import sys
import sly.yacc as yacc
from mparser import MyParser
from TreePrinter import TreePrinter

# from TypeChecker import TypeChecker

if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = MyParser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner)

    # # Below code shows how to use visitor
    # typeChecker = TypeChecker()
    # typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
