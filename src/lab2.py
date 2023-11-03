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
    text = """
A = zeros(5); # create 5x5 matrix filled with zeros
D = A.+B' ;   # add element-wise A with transpose of B

for j = 1:10 
    print j;
"""
    tokens = lexer.tokenize(text=text)
    result = parser.parse(tokens)
    print(result)
