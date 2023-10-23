from sly import Parser
from scanner import MyLexer


class MyParser(Parser):
    tokens = MyLexer.tokens

    @_("expr ADD term")
    def expr(self, p):
        pass
