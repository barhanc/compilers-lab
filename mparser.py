from sly import Parser
from scanner import MyLexer
from AST import *


class MyParser(Parser):
    debugfile = "parser.out"
    tokens = MyLexer.tokens
    start = "statementseq"

    # ==============================================================================================
    # Statements

    @_("statement statementseq")
    def statementseq(self, p):
        return [p.statement] + p.statementseq

    @_("statement")
    def statementseq(self, p):
        return [p.statement]

    @_('PRINT exprseq ";"')
    def statement(self, p):
        return Print(p.exprseq, lineno=p.lineno)

    @_('RETURN exprseq ";"')
    def statement(self, p):
        return Return(p.exprseq, lineno=p.lineno)

    @_('BREAK ";"')
    def statement(self, p):
        return Break(lineno=p.lineno)

    @_('CONTINUE ";"')
    def statement(self, p):
        return Continue(lineno=p.lineno)

    assignment = [
        'ID "=" expr ";"',
        'ID IADD expr ";"',
        'ID ISUB expr ";"',
        'ID IMUL expr ";"',
        'ID IDIV expr ";"',
    ]

    @_(*assignment)
    def statement(self, p):
        return Assignment(id=Id(p[0]), op=p[1], val=p[2], lineno=p.lineno)

    ref_assignment = [
        'ID "[" exprseq "]" "=" expr ";"',
        'ID "[" exprseq "]" IADD expr ";"',
        'ID "[" exprseq "]" ISUB expr ";"',
        'ID "[" exprseq "]" IMUL expr ";"',
        'ID "[" exprseq "]" IDIV expr ";"',
    ]

    @_(*ref_assignment)
    def statement(self, p):
        return RefAssignment(op=p[4], id=Id(p[0]), idx=p.exprseq, val=p.expr, lineno=p.lineno)

    @_(
        'IF "(" expr ")" statement %prec IFX',
        'IF "(" expr ")" statement ELSE statement',
    )
    def statement(self, p):
        return If(p[2], p[4], p[6] if 6 < len(p) else None, lineno=p.lineno)

    @_('WHILE "(" expr ")" statement')
    def statement(self, p):
        return While(condition=p[2], body=p[4], lineno=p.lineno)

    @_('FOR ID "=" expr ":" expr statement')
    def statement(self, p):
        return For(id=Id(p[1]), start=p[3], end=p[5], body=p[6], lineno=p.lineno)

    @_('"{" statementseq "}"')
    def statement(self, p):
        return Block(p.statementseq)

    # Expressions

    precedence = (
        ("nonassoc", EQ, NE, GT, GE, LT, LE),
        ("left", ADD, SUB, DADD, DSUB),
        ("left", MUL, DIV, DMUL, DDIV),
        ("right", UMINUS),
        ("left", "'"),
        ("nonassoc", IFX),
        ("nonassoc", ELSE),
    )

    # In this case, %prec UMINUS overrides the default rule precedence–setting it to that of UMINUS
    # in the precedence specifier.
    @_("SUB expr %prec UMINUS")
    def expr(self, p):
        return UnaryExpr(operator="SUB", operand=p.expr, lineno=p.lineno)

    @_("""expr "'" """)
    def expr(self, p):
        return UnaryExpr(operator="TRANSPOSE", operand=p.expr, lineno=p.lineno)

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
        return BinExpr(p[1], p[0], p[2], lineno=p.lineno)

    @_('"(" expr ")"')
    def expr(self, p):
        return Expression(p[1], lineno=p.lineno)

    @_("ID")
    def expr(self, p):
        return Id(p[0], lineno=p.lineno)

    @_("INTNUM")
    def expr(self, p):
        return IntNum(int(p[0]), lineno=p.lineno)

    @_("FLOATNUM")
    def expr(self, p):
        return FloatNum(float(p[0]), lineno=p.lineno)

    @_("STRING")
    def expr(self, p):
        return String(p[0], lineno=p.lineno)

    @_("expr")
    def exprseq(self, p):
        return ExpressionSeq([p.expr], lineno=p.lineno)

    @_('exprseq "," expr')
    def exprseq(self, p):
        node = p.exprseq
        node.elements.append(p.expr)
        return node

    @_(
        'EYE "(" expr ")"',
        'ONES "(" exprseq ")"',
        'ZEROS "(" exprseq ")"',
    )
    def expr(self, p):
        return BuiltinExpr(id=p[0], arg=p[2], lineno=p.lineno)

    @_('expr "[" exprseq "]"')
    def expr(self, p):
        return Reference(p.expr, p.exprseq, lineno=p.lineno)

    @_('"[" exprseq "]"')
    def array(self, p):
        return Vector(elements=p.exprseq.elements, lineno=p.lineno)

    @_("array")
    def expr(self, p):
        return p.array
