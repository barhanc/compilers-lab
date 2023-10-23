import sys
import scanner  # scanner.py is a file you create, (it is not an external library)


if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.MyLexer()

    # Tokenize
    for tok in lexer.tokenize(text):
        print("%d: %s(%s)" % (tok.lineno, tok.type, tok.value))
