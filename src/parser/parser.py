# parser/parser.py
from parser.base import ParserBase
from parser.expressions import ExpressionParser
from parser.lists import ListParser
from parser.functions import FunctionParser
from parser.control import ControlParser
from parser.statments import StatementParser
from node import *
from error import *


class Parser(
    ParserBase,
    ExpressionParser,
    ListParser,
    FunctionParser,
    ControlParser,
    StatementParser,
):
    def parse_statement(self):
        t = self.current()[0]

        if t == "PRINT":
            return self.parse_print_statement()
        if t == "IF":
            return self.parse_conditionals()
        if t == "FUN":
            return self.parse_function()
        if t == "IDENTIFIER":
            return self.parse_assignment_or_expr_statement()

        raise unexpected_token(self)

    def parse(self):
        stmts = []
        while self.current()[0] is not None:
            stmts.append(self.parse_statement())
        return stmts
