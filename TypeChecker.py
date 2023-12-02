import AST
import numpy as np

from collections import defaultdict
from SymbolTable import SymbolTable, Symbol

ttypes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

ttypes["+"]["int"]["int"] = "int"
ttypes["+"]["int"]["float"] = "float"
ttypes["+"]["float"]["int"] = "float"
ttypes["+"]["float"]["float"] = "float"
ttypes["+"]["str"]["str"] = "str"

ttypes["-"]["int"]["int"] = "int"
ttypes["-"]["int"]["float"] = "float"
ttypes["-"]["float"]["int"] = "float"
ttypes["-"]["float"]["float"] = "float"

ttypes["*"]["int"]["int"] = "int"
ttypes["*"]["int"]["float"] = "float"
ttypes["*"]["float"]["int"] = "float"
ttypes["*"]["float"]["float"] = "float"

ttypes["/"]["int"]["int"] = "float"
ttypes["/"]["int"]["float"] = "float"
ttypes["/"]["float"]["int"] = "float"
ttypes["/"]["float"]["float"] = "float"

ttypes[">"]["int"]["int"] = "bool"
ttypes[">"]["int"]["float"] = "bool"
ttypes[">"]["float"]["int"] = "bool"
ttypes[">"]["float"]["float"] = "bool"

ttypes["<"]["int"]["int"] = "bool"
ttypes["<"]["int"]["float"] = "bool"
ttypes["<"]["float"]["int"] = "bool"
ttypes["<"]["float"]["float"] = "bool"

ttypes[">="]["int"]["int"] = "bool"
ttypes[">="]["int"]["float"] = "bool"
ttypes[">="]["float"]["int"] = "bool"
ttypes[">="]["float"]["float"] = "bool"

ttypes["<="]["int"]["int"] = "bool"
ttypes["<="]["int"]["float"] = "bool"
ttypes["<="]["float"]["int"] = "bool"
ttypes["<="]["float"]["float"] = "bool"

ttypes["=="]["int"]["int"] = "bool"
ttypes["=="]["int"]["float"] = "bool"
ttypes["=="]["float"]["int"] = "bool"
ttypes["=="]["float"]["float"] = "bool"

ttypes["!="]["int"]["int"] = "bool"
ttypes["!="]["int"]["float"] = "bool"
ttypes["!="]["float"]["int"] = "bool"
ttypes["!="]["float"]["float"] = "bool"

ttypes[".+"]["vector[int]"]["vector[int]"] = "vector[int]"
ttypes[".+"]["vector[float]"]["vector[int]"] = "vector[float]"
ttypes[".+"]["vector[int]"]["vector[float]"] = "vector[float]"
ttypes[".+"]["vector[float]"]["vector[float]"] = "vector[float]"

ttypes[".-"]["vector[int]"]["vector[int]"] = "vector[int]"
ttypes[".-"]["vector[float]"]["vector[int]"] = "vector[float]"
ttypes[".-"]["vector[int]"]["vector[float]"] = "vector[float]"
ttypes[".-"]["vector[float]"]["vector[float]"] = "vector[float]"

ttypes[".*"]["vector[int]"]["vector[int]"] = "vector[int]"
ttypes[".*"]["vector[float]"]["vector[int]"] = "vector[float]"
ttypes[".*"]["vector[int]"]["vector[float]"] = "vector[float]"
ttypes[".*"]["vector[float]"]["vector[float]"] = "vector[float]"

ttypes["./"]["vector[int]"]["vector[int]"] = "vector[float]"
ttypes["./"]["vector[float]"]["vector[int]"] = "vector[float]"
ttypes["./"]["vector[int]"]["vector[float]"] = "vector[float]"
ttypes["./"]["vector[float]"]["vector[float]"] = "vector[float]"

ttypes["+="]["int"]["int"] = "int"
ttypes["+="]["int"]["float"] = "float"
ttypes["+="]["float"]["int"] = "float"
ttypes["+="]["float"]["float"] = "float"
ttypes["+="]["str"]["str"] = "str"

ttypes["-="]["int"]["int"] = "int"
ttypes["-="]["int"]["float"] = "float"
ttypes["-="]["float"]["int"] = "float"
ttypes["-="]["float"]["float"] = "float"

ttypes["*="]["int"]["int"] = "int"
ttypes["*="]["int"]["float"] = "float"
ttypes["*="]["float"]["int"] = "float"
ttypes["*="]["float"]["float"] = "float"

ttypes["/="]["int"]["int"] = "float"
ttypes["/="]["int"]["float"] = "float"
ttypes["/="]["float"]["int"] = "float"
ttypes["/="]["float"]["float"] = "float"

ERR = "\033[91m" + "Error" + "\033[0m"


class NodeVisitor:
    def __init__(self) -> None:
        self.scope: SymbolTable = SymbolTable(None, "global")
        self.loop_cnt = 0

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def visit_Block(self, node: AST.Block):
        for statement in node.statements:
            self.visit(statement)

    def visit_Id(self, node: AST.Id):
        return self.scope.get(node.name)

    def visit_IntNum(self, node: AST.IntNum):
        return Symbol("int", value=node.value)

    def visit_FloatNum(self, node: AST.FloatNum):
        return Symbol("float", value=node.value)

    def visit_String(self, node: AST.String):
        return Symbol("str", value=node.value)

    def visit_Expression(self, node: AST.Expression):
        return self.visit(node.value)

    def visit_ExpressionSeq(self, node: AST.ExpressionSeq):
        syms = []
        for expr in node.elements:
            syms.append(self.visit(expr))
        return syms

    def visit_UnaryExpr(self, node: AST.UnaryExpr):
        sym = self.visit(node.operand)

        if node.operator == "-" and sym.type in {"str", "bool"}:
            print(
                ERR
                + f" (Line {node.lineno}) "
                + f"Invalid operand {sym.type} for operator {node.operand}"
            )
            return None

        if node.operand == "'" and sym.type[:6] != "vector" and len(sym.dims) != 2:
            print(
                ERR
                + f" (Line {node.lineno}) "
                + f"Invalid operand {sym.type} for operator {node.operand}"
            )
            return None

        match node.operator:
            case "-":
                return Symbol(sym.type, -sym.value, sym.dims)
            case "'":
                return Symbol(sym.type, np.transpose(sym.value), sym.dims[::-1])

    def visit_BinExpr(self, node: AST.BinExpr):
        sym1 = self.visit(node.left)
        sym2 = self.visit(node.right)
        op = node.op

        if ttypes[op][sym1.type][sym2.type] == "":
            print(
                ERR
                + f" (Line {node.lineno}) "
                + f"Invalid types: {sym1.type} {sym2.type} for operand {op}"
            )
            return None

        if sym1.dims != sym2.dims:
            print(
                ERR
                + f" (Line {node.lineno}) "
                + f"Incompatible dimensions: {sym1.dims} {sym2.dims}"
            )
            return None

        value = None
        match op:
            case "+" | ".+":
                value = sym1.value + sym2.value
            case "-" | ".-":
                value = sym1.value - sym2.value
            case "*" | ".*":
                value = sym1.value + sym2.value
            case "*" | ".*":
                value = sym1.value + sym2.value
            case "<":
                value = sym1.value < sym2.value
            case ">":
                value = sym1.value > sym2.value
            case ">=":
                value = sym1.value >= sym2.value
            case "<=":
                value = sym1.value <= sym2.value
            case "==":
                value = sym1.value == sym2.value
            case "!=":
                value = sym1.value == sym2.value

        return Symbol(
            ttypes[op][sym1.type][sym2.type],
            value,
            sym1.dims,
        )

    def visit_BuiltinExpr(self, node: AST.BuiltinExpr):
        match node.id:
            case "zeros":
                syms = self.visit(node.arg)
                for sym in syms:
                    if sym.type != "int":
                        print(
                            ERR + f" (Line {node.lineno}) " + f"Invalid argument type: {sym.type}"
                        )
                        return None
                return Symbol(
                    "vector[float]",
                    value=np.zeros([sym.value for sym in syms], dtype=float),
                    dims=[sym.value for sym in syms],
                )

            case "ones":
                syms = self.visit(node.arg)
                for sym in syms:
                    if sym.type != "int":
                        print(
                            ERR + f" (Line {node.lineno}) " + f"Invalid argument type: {sym.type}"
                        )
                        return None
                return Symbol(
                    "vector[float]",
                    value=np.ones([sym.value for sym in syms], dtype=float),
                    dims=[sym.value for sym in syms],
                )

            case "eye":
                sym = self.visit(node.arg)
                if sym.type != "int":
                    print(ERR + f" (Line {node.lineno}) " + f"Invalid argument type: {sym.type}")
                    return None
                return Symbol(
                    "vector[float]",
                    value=np.eye(sym.value, dtype=float),
                    dims=[sym.value, sym.value],
                )

    def visit_Vector(self, node: AST.Vector):
        values, types, dims = [], [], []
        for element in node.elements:
            sym = self.visit(element)
            values.append(sym.value)
            types.append(sym.type)
            dims.append(sym.dims)

        if len(set(types)) != 1:
            print(ERR + f" (Line {node.lineno}) " + f"Heterogeneous arrays are not supported")
            return None

        if len(set(tuple(dim) if dim is not None else dim for dim in dims)) != 1:
            print(ERR + f" (Line {node.lineno}) " + f"Incompatible dimensions")
            return None

        return Symbol(
            type=f"vector[{types[0].replace(']', '').split('[')[-1]}]",
            value=np.array(values),
            dims=[len(dims), *dims[0]] if dims[0] is not None else [len(dims)],
        )

    def visit_Reference(self, node: AST.Reference):
        sym = self.visit(node.expr)
        idxs = self.visit(node.idx)

        if len(sym.dims) != len(idxs):
            print(ERR + f" (Line {node.lineno}) " + "Incompatible array axes")
            return None

        for i, idx in enumerate(idxs):
            if idx.value < 0 or idx.value >= sym.dims[i]:
                print(ERR + f" (Line {node.lineno}) " + f"Index out of bounds")
                return None

        return Symbol(
            sym.type.split("[")[-1][:-1],
            sym.value[[idx.value for idx in idxs]],
        )

    def visit_Assignment(self, node: AST.Assignment):
        if node.op == "=":
            self.scope.put(node.id.name, self.visit(node.val))
        else:
            sym_l = self.scope.get(node.id.name)
            sym_r = self.visit(node.val)

            if ttypes[node.op[:1]][sym_l.type][sym_r.type] == "":
                print(
                    ERR
                    + f" (Line {node.lineno}) "
                    + f"Invalid types: {sym_l.type} {sym_r.type} for operand {node.op}"
                )
                return None

            if sym_l.dims != sym_r.dims:
                print(ERR + f" (Line {node.lineno}) " + "Incompatible dimension")
                return None

            value = None
            match node.op[:1]:
                case "+":
                    value = sym_l.value + sym_r.value
                case "-":
                    value = sym_l.value - sym_r.value
                case "*":
                    value = sym_l.value * sym_r.value
                case "/":
                    value = sym_l.value / sym_r.value

            self.scope.put(
                node.id.name,
                Symbol(
                    ttypes[node.op[:1]][sym_l.type][sym_r.type],
                    value,
                    sym_l.dims,
                ),
            )

    def visit_RefAssignment(self, node: AST.RefAssignment):
        pass

    def visit_If(self, node: AST.If):
        self.scope = self.scope.pushScope("if")
        self.visit(node.condition)
        self.visit(node.body)
        self.scope = self.scope.popScope()

        if node.else_body is not None:
            self.scope = self.scope.pushScope("else")
            self.visit(node.else_body)
            self.scope = self.scope.popScope()

    def visit_Return(self, node: AST.Return):
        self.visit(node.exprseq)

    def visit_Print(self, node: AST.Print):
        self.visit(node.exprseq)

    def visit_Break(self, node: AST.Break):
        if self.loop_cnt == 0:
            print(ERR + f" (Line {node.lineno}) " + "'break' outside loop")

    def visit_Continue(self, node: AST.Continue):
        if self.loop_cnt == 0:
            print(ERR + f" (Line {node.lineno}) " + "'continue' outside loop")

    def visit_For(self, node: AST.For):
        self.scope = self.scope.pushScope("for")
        self.loop_cnt += 1
        sym_i = self.visit(node.start)
        sym_j = self.visit(node.end)

        if sym_i.type != "int" or sym_j.type != "int":
            print(ERR + f" (Line {node.lineno}) " + "Invalid type in range")
            return None

        self.scope.put(node.id.name, Symbol("int", value=sym_i.value))
        self.visit(node.body)
        self.loop_cnt -= 1
        self.scope = self.scope.popScope()

    def visit_While(self, node: AST.While):
        self.scope = self.scope.pushScope("while")
        self.loop_cnt += 1
        self.visit(node.condition)
        self.visit(node.body)
        self.loop_cnt -= 1
        self.scope = self.scope.popScope()
