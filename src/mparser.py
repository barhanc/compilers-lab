from sly import Parser
from scanner import MyLexer


class MyParser(Parser):
    debugfile = "parser.out"
    tokens = MyLexer.tokens
    start = "program"

    @_("statement_sequence")
    def program(self, p):
        return p

    precedence = (
        ("right", "=", IADD, ISUB, IMUL, IDIV),
        ("nonassoc", ":"),
        ("left", EQ, NE, GT, GE, LT, LE),
        ("left", UMINUS),
        ("left", ADD, SUB, DADD, DSUB),
        ("left", MUL, DIV, DMUL, DDIV),
        ("left", TRANSPOSE),
        ("left", INDEX),
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
        'expr ":" expr',
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

    @_('expr "[" exprseq "]" %prec INDEX')
    def expr(self, p):
        return p

    @_('"[" elements "]"')
    def array(self, p):
        return p

    @_("expr", 'elements "," expr')
    def elements(self, p):
        return p

    @_("array")
    def expr(self, p):
        return p

    # ==============================================================================================
    # Statements
    # ==============================================================================================

    @_('PRINT exprseq ";"', 'RETURN exprseq ";"')
    def statement(self, p):
        return p

    @_('BREAK ";"', 'CONTINUE ";"')
    def statement(self, p):
        return p

    assignment = [
        'expr "=" expr ";"',
        'expr IADD expr ";"',
        'expr ISUB expr ";"',
        'expr IMUL expr ";"',
        'expr IDIV expr ";"',
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

    @_('FOR ID "=" exprseq statement')
    def statement(self, p):
        return p

    @_('"{" statement_sequence "}"')
    def statement(self, p):
        return p

    @_("statement statement_sequence", "statement")
    def statement_sequence(self, p):
        return p
