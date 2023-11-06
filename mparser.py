from sly import Parser
from scanner import MyLexer


class MyParser(Parser):
    debugfile = "parser.out"
    tokens = MyLexer.tokens
    start = "statementseq"

    # ==============================================================================================
    # Statements

    @_("statement statementseq", "statement")
    def statementseq(self, p):
        return p

    @_('PRINT exprseq ";"', 'RETURN exprseq ";"')
    def statement(self, p):
        return p

    @_('BREAK ";"', 'CONTINUE ";"')
    def statement(self, p):
        return p

    assignment = [
        'ID "=" expr ";"',
        'ID IADD expr ";"',
        'ID ISUB expr ";"',
        'ID IMUL expr ";"',
        'ID IDIV expr ";"',
        'ID "[" exprseq "]" "=" expr ";"',
        'ID "[" exprseq "]" IADD expr ";"',
        'ID "[" exprseq "]" ISUB expr ";"',
        'ID "[" exprseq "]" IMUL expr ";"',
        'ID "[" exprseq "]" IDIV expr ";"',
    ]

    @_(*assignment)
    def statement(self, p):
        return p

    @_(
        'IF "(" expr ")" statement %prec IFX',
        'IF "(" expr ")" statement ELSE statement',
    )
    def statement(self, p):
        return p

    @_('WHILE "(" expr ")" statement')
    def statement(self, p):
        return p

    @_('FOR ID "=" expr ":" expr statement')
    def statement(self, p):
        return p

    @_('"{" statementseq "}"')
    def statement(self, p):
        return p

    # Expressions

    precedence = (
        ("nonassoc", EQ, NE, GT, GE, LT, LE),
        ("left", ADD, SUB, DADD, DSUB),
        ("left", MUL, DIV, DMUL, DDIV),
        ("right", UMINUS),
        ("left", TRANSPOSE),
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
    )

    binary_expr = [
        "expr ADD expr",
        "expr SUB expr",
        "expr MUL expr",
        "expr DIV expr",
        "expr DADD expr",
        "expr DSUB expr",
        "expr DMUL expr",
        "expr DDIV expr",
        "expr EQ expr",
        "expr NE expr",
        "expr GT expr",
        "expr GE expr",
        "expr LT expr",
        "expr LE expr",
    ]

    @_(*binary_expr)
    def expr(self, p):
        return p

    @_('"(" expr ")"')
    def expr(self, p):
        return p

    # In this case, %prec UMINUS overrides the default rule precedence–setting it to that of UMINUS
    # in the precedence specifier.
    @_("SUB expr %prec UMINUS")
    def expr(self, p):
        return p

    @_("""expr "'" %prec TRANSPOSE""")
    def expr(self, p):
        return p

    @_(
        "ID",
        "INTNUM",
        "FLOATNUM",
        "STRING",
    )
    def expr(self, p):
        return p

    @_("expr", ' exprseq "," expr')
    def exprseq(self, p):
        return p

    @_(
        'EYE "(" expr ")"',
        'ONES "(" expr ")"',
        'ZEROS "(" expr ")"',
    )
    def expr(self, p):
        return p

    @_('expr "[" exprseq "]"')
    def expr(self, p):
        return p

    @_('"[" exprseq "]"')
    def array(self, p):
        return p

    @_("array")
    def expr(self, p):
        return p
