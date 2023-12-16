from dataclasses import dataclass
from typing import Any, Optional, List


@dataclass
class Node:
    pass


@dataclass
class Statement(Node):
    pass


@dataclass
class Block(Node):
    statements: List[Statement]


@dataclass
class Id(Node):
    name: str
    lineno: int = 0


@dataclass
class IntNum(Node):
    value: int
    lineno: int = 0


@dataclass
class FloatNum(Node):
    value: float
    lineno: int = 0


@dataclass
class String(Node):
    value: str
    lineno: int = 0


@dataclass
class Expression(Node):
    value: Any
    lineno: int = 0


@dataclass
class ExpressionSeq(Node):
    elements: List[Expression]
    lineno: int = 0


@dataclass
class UnaryExpr(Node):
    operator: str
    operand: Expression
    lineno: int = 0


@dataclass
class BinExpr(Node):
    op: str
    left: Expression
    right: Expression
    lineno: int = 0


@dataclass
class BuiltinExpr(Node):
    id: str
    arg: Expression
    lineno: int = 0


@dataclass
class Vector(Node):
    elements: List[Any]
    lineno: int = 0


@dataclass
class Reference(Node):
    expr: Expression
    idx: ExpressionSeq
    lineno: int = 0


@dataclass
class Assignment(Statement):
    id: Id
    op: str
    val: Expression
    lineno: int = 0


@dataclass
class RefAssignment(Statement):
    op: str
    id: Id
    idx: ExpressionSeq
    val: Expression
    lineno: int = 0


@dataclass
class If(Statement):
    condition: Expression
    body: Statement
    else_body: Optional[Statement]
    lineno: int = 0


@dataclass
class While(Statement):
    condition: Expression
    body: Statement
    lineno: int = 0


@dataclass
class For(Statement):
    id: Id
    start: Expression
    end: Expression
    body: Statement
    lineno: int = 0


@dataclass
class Return(Statement):
    exprseq: ExpressionSeq
    lineno: int = 0


@dataclass
class Print(Statement):
    exprseq: ExpressionSeq
    lineno: int = 0


@dataclass
class Break(Statement):
    lineno: int = 0


@dataclass
class Continue(Statement):
    lineno: int = 0
