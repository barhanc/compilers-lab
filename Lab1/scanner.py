from sly import Lexer


class MyLexer(Lexer):
    # Set of token names.
    # fmt: off
    tokens = {FLOATNUM, INTNUM, STRING, ID, WHILE, IF, ELSE, PRINT, ADD, SUB,
            MUL, DIV, DADD, DSUB, DMUL, DDIV, IADD, ISUB, IMUL, IDIV, EQ, LT,
            LE, GT, GE, NE, FOR, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES}
    # fmt: on

    literals = {"=", "(", ")", "{", "}", "[", "]", ":", ";", ",", "'"}

    # Regular expression rules for tokens
    DADD = r"\.\+"
    DSUB = r"\.-"
    DMUL = r"\.\*"
    DDIV = r"\./"
    IADD = r"\+="
    ISUB = r"-="
    IMUL = r"\*="
    IDIV = r"/="
    ADD = r"\+"
    SUB = r"-"
    MUL = r"\*"
    DIV = r"/"
    EQ = r"=="
    LE = r"<="
    LT = r"<"
    GE = r">="
    GT = r">"
    NE = r"!="

    @_(r"[+-]?([0-9]+\.([0-9]*)?|[.][0-9]+)(E[+-]?\d+)?")
    def FLOATNUM(self, t):
        e = t.value.find("E")
        if e == -1:
            t.value = float(t.value)
        else:
            t.value = float(t.value[:e]) * 10 ** int(t.value[e + 1 :])

        return t

    @_(r"\d+")
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'".*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    # Identifiers and keywords
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["if"] = IF
    ID["else"] = ELSE
    ID["for"] = FOR
    ID["while"] = WHILE
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["print"] = PRINT
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES

    # Ignored characters
    ignore = " \t"
    ignore_comment = r"\#.*"

    # Line number tracking
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print("\033[91m" + "Line %d: Bad character %r" % (self.lineno, t.value[0]) + "\033[0m")
        self.index += 1
