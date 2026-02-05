# parser/expressions.py
from node import *
from error import unexpected_token

class ExpressionParser:
    def parse_parens(self, parse_fn):
        self.eat("LPAREN")
        node = parse_fn()
        self.eat("RPAREN")
        return node
    # --- Atoms (lowest-level expressions) ---
    def parse_atom(self):
        type_, value = self.current()

        if type_ == "NUMBER":
            self.eat("NUMBER")
            return Number(int(value))

        if type_ == "STRING":
            self.eat("STRING")
            return String(value)

        if type_ == "INPUT":
            self.eat("INPUT")
            prompt = None
            if self.current()[0] == "LPAREN":
                self.eat("LPAREN")
                if self.current()[0] == "STRING":
                    prompt = self.eat("STRING")
                self.eat("RPAREN")
            return Input(prompt)

        if type_ == "IDENTIFIER":
            name = self.eat("IDENTIFIER")

            if self.current()[0] == "DOT":
                self.eat("DOT")
                member = self.eat("IDENTIFIER")
                # If a call follows the member (e.g. Module.member(...))
                # return a FunctionCall whose name is a ModuleAccess node.
                if self.current()[0] == "LPAREN":
                    return self.parse_function_call(ModuleAccess(name, member))
                return ModuleAccess(name, member)
            # function call: f(...)
            if self.current()[0] == "LPAREN":
                return self.parse_function_call(name)

            # list access: a[expr]
            if self.current()[0] == "SLBRACKET":
                self.eat("SLBRACKET")
                index = self.parse_logical()
                self.eat("SRBRACKET")
                return ListAccessPos(name, index)

            return Variable(name)

        # list literal: [1, 2, 3]
        if type_ == "SLBRACKET":
            elements = self.parse_list()
            return ListAssign(None, elements)

        # parenthesized expression
        if type_ == "LPAREN":
            self.eat("LPAREN")
            expr = self.parse_logical()
            self.eat("RPAREN")
            return expr

        raise unexpected_token(self)

    # --- Operator precedence ---
    def parse_term(self):
        left = self.parse_atom()
        while self.current()[0] in ("MULT", "DIV"):
            op = self.eat(self.current()[0])
            right = self.parse_atom()
            left = BinOp(left, op, right)
        return left

    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] in ("PLUS", "MINUS"):
            op = self.eat(self.current()[0])
            right = self.parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_comparison(self):
        left = self.parse_expression()
        while self.current()[0] in ("EQ", "NEQ", "GT", "LT", "GTE", "LTE"):
            op = self.eat(self.current()[0])
            right = self.parse_expression()
            left = BinOp(left, op, right)
        return left

    def parse_logical(self):
        left = self.parse_comparison()
        while self.current()[0] in ("AND", "OR"):
            op = self.eat(self.current()[0])
            right = self.parse_comparison()
            left = BinOp(left, op, right)
        return left
