import AST
import sys
import SymbolTable
import numpy as np

from visit import *
from Memory import *
from Exceptions import *

sys.setrecursionlimit(10000)

bin_operators = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x @ y if isinstance(x, np.ndarray) else x * y,
    "/": lambda x, y: x / y,
    ".+": lambda x, y: x + y,
    ".-": lambda x, y: x - y,
    ".*": lambda x, y: x * y,
    "./": lambda x, y: x / y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "=": lambda x, y: y,
}

unary_operators = {
    "'": lambda x: x.T,
    "-": lambda x: -x,
}


class Interpreter(object):
    def __init__(self) -> None:
        self.memory_stack = MemoryStack()

    @on("node")
    def visit(self, node):
        pass

    # ===============================================================
    @when(AST.Block)
    def visit(self, node: AST.Block):
        for statement in node.statements:
            self.visit(statement)

    @when(AST.Print)
    def visit(self, node: AST.Print):
        print(*self.visit(node.exprseq))

    # ===============================================================

    @when(AST.Expression)
    def visit(self, node: AST.Expression):
        return self.visit(node.value)

    @when(AST.ExpressionSeq)
    def visit(self, node: AST.ExpressionSeq):
        return [self.visit(expr) for expr in node.elements]

    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        return node.value

    @when(AST.String)
    def visit(self, node: AST.String):
        return node.value

    @when(AST.Vector)
    def visit(self, node: AST.Vector):
        return np.array([self.visit(el) for el in node.elements])

    @when(AST.Reference)
    def visit(self, node: AST.Reference):
        return self.visit(node.expr)[*self.visit(node.idx)]

    @when(AST.Id)
    def visit(self, node: AST.Id):
        return self.memory_stack.get(node.name)

    # ===============================================================

    @when(AST.UnaryExpr)
    def visit(self, node: AST.UnaryExpr):
        return unary_operators[node.operator](self.visit(node.operand))

    @when(AST.BinExpr)
    def visit(self, node: AST.BinExpr):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)

        return bin_operators[node.op](r1, r2)

    @when(AST.BuiltinExpr)
    def visit(self, node: AST.BuiltinExpr):
        match node.id:
            case "zeros":
                return np.zeros(self.visit(node.arg))
            case "ones":
                return np.ones(self.visit(node.arg))
            case "eye":
                return np.eye(self.visit(node.arg))
            case _:
                return None

    # ===============================================================

    @when(AST.Assignment)
    def visit(self, node: AST.Assignment):
        self.memory_stack.set(
            node.id.name,
            bin_operators[node.op[0]](self.visit(node.id), self.visit(node.val)),
        )

    @when(AST.RefAssignment)
    def visit(self, node: AST.RefAssignment):
        val = self.visit(node.id)
        val[*self.visit(node.idx)] = bin_operators[node.op[0]](
            val[*self.visit(node.idx)],
            self.visit(node.val),
        )
        self.memory_stack.set(node.id.name, val)

    # ===============================================================

    @when(AST.If)
    def visit(self, node: AST.If):
        self.memory_stack.push(Memory("if"))
        if self.visit(node.condition):
            self.visit(node.body)
        elif node.else_body is not None:
            self.visit(node.else_body)
        self.memory_stack.pop()

    @when(AST.For)
    def visit(self, node: AST.For):
        self.memory_stack.push(Memory("for"))
        i_name = node.id.name
        for i in range(self.visit(node.start), self.visit(node.end)):
            try:
                self.memory_stack.set(i_name, i)
                self.visit(node.body)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()

    # simplistic while loop interpretation
    @when(AST.While)
    def visit(self, node: AST.While):
        self.memory_stack.push(Memory("while"))
        cond = self.visit(node.condition)

        while cond:
            try:
                self.visit(node.body)
                cond = self.visit(node.condition)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory_stack.pop()

    @when(AST.Break)
    def visit(self, node: AST.Break):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node: AST.Continue):
        raise ContinueException()
