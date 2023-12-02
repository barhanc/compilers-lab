from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.name}")

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.value}")

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.value}")

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.value}")

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(AST.Expression)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.val}")

    @addToClass(AST.ExpressionSeq)
    def printTree(self, indent=0):
        for expr in self.elements:
            expr.printTree(indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.op}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.operator}")
        self.operand.printTree(indent + 1)

    @addToClass(AST.BuiltinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.id}")
        self.arg.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("|  " * indent + f"VECTOR")
        for element in self.elements:
            element.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.op}")
        self.id.printTree(indent + 1)
        self.val.printTree(indent + 1)

    @addToClass(AST.Reference)
    def printTree(self, indent=0):
        print("|  " * indent + f"REF")
        self.expr.printTree(indent + 1)
        self.idx.printTree(indent + 1)

    @addToClass(AST.RefAssignment)
    def printTree(self, indent=0):
        print("|  " * indent + f"{self.op}")
        self.ref.printTree(indent + 1)
        self.val.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.condition.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.body.printTree(indent + 1)
        if self.else_body is not None:
            print("|  " * indent + "ELSE")
            self.else_body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.id.printTree(indent + 1)
        print("|  " * (indent + 1) + "RANGE")
        self.start.printTree(indent + 2)
        self.end.printTree(indent + 2)
        self.body.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + f"RETURN")
        self.exprseq.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("|  " * indent + f"PRINT")
        self.exprseq.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|  " * indent + f"BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|  " * indent + f"CONTINUE")
