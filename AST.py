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


@dataclass
class IntNum(Node):
    value: int


@dataclass
class FloatNum(Node):
    value: float


@dataclass
class String(Node):
    value: str


@dataclass
class Expression(Node):
    value: Any
    type: Optional[str] = None


@dataclass
class ExpressionSeq(Node):
    elements: List[Expression]


@dataclass
class UnaryExpr(Node):
    operator: str
    operand: Expression


@dataclass
class BinExpr(Node):
    op: str
    left: Expression
    right: Expression


@dataclass
class BuiltinExpr(Node):
    id: str
    arg: Expression


@dataclass
class Vector(Node):
    elements: List[Any]


@dataclass
class Reference(Node):
    expr: Expression
    idx: ExpressionSeq


@dataclass
class Assignment(Statement):
    id: str
    op: str
    val: Expression


@dataclass
class RefAssignment(Statement):
    op: str
    ref: Reference
    val: Expression


@dataclass
class If(Statement):
    condition: Expression
    body: Statement
    else_body: Optional[Statement]


@dataclass
class While(Statement):
    condition: Expression
    body: Statement


@dataclass
class For(Statement):
    id: Id
    start: Expression
    end: Expression
    body: Statement


# TODO: Change Keyword /Call to Print, Return, Break, Continue
@dataclass
class OutputKeyword(Statement):
    id: str
    exprseq: ExpressionSeq


@dataclass
class ControlTransferKeyword(Statement):
    id: str


@dataclass
class Error(Node):
    pass
