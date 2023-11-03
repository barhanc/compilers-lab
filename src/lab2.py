import sys
from scanner import MyLexer
from mparser import MyParser

if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example3.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = MyParser()
    lexer = MyLexer()
    text = file.read()
    tokens = lexer.tokenize(text=text)
    result = parser.parse(tokens)
    print(result)
