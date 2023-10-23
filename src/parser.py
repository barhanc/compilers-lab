#!/usr/bin/python

from scanner import MyLexer
from sly import Parser


class MyParser(Parser):
    tokens = MyLexer.tokens
