from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Symbol:
    type: str
    value: Any
    dims: Optional[list[int]] = None


class SymbolTable(object):
    def __init__(self, parent, name):
        # parent scope and symbol table name
        self.parent_scope = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol: Symbol):
        # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name) -> Symbol:
        # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent_scope is not None:
            return self.parent_scope.get(name)
        else:
            print(f"'{name}' not found in scope!")
            return None

    def getParentScope(self):
        return self.parent_scope

    def pushScope(self, name):
        return SymbolTable(parent=self, name=name)

    def popScope(self):
        return self.parent_scope
