from node import *
from error import unexpected_token, ParseError

class StatementParser:
    # --- Expression statements ---
    def parse_expression_statement(self):
        expr = self.parse_logical()
        self.eat("SEMICOLON")
        return expr

    # --- Print ---
    def parse_print_statement(self):
        self.eat("PRINT")
        expr = self.parse_parens(self.parse_logical)
        self.eat("SEMICOLON")
        return Print(expr)

    # --- Input ---
    def parse_input_statement(self):
        self.eat("INPUT")
        prompt = None
        if self.current()[0] == "LPAREN":
            self.eat("LPAREN")
            if self.current()[0] == "STRING":
                prompt = self.eat("STRING")
            self.eat("RPAREN")
        self.eat("SEMICOLON")
        return Input(prompt)

    # --- Assignment OR expression ---
    def parse_assignment_or_expr_statement(self):
        save_pos = self.pos
        try:
            name = self.eat("IDENTIFIER")
            lhs = name

            # list assignment: a[expr] = ...
            if self.current()[0] == "SLBRACKET":
                self.eat("SLBRACKET")
                index_expr = self.parse_logical()
                self.eat("SRBRACKET")
                lhs = ListAccessPos(name, index_expr)

            if self.current()[0] == "EQUAL":
                self.eat("EQUAL")
                expr = self.parse_logical()
                self.eat("SEMICOLON")

                if isinstance(lhs, ListAccessPos):
                    return AssignListElement(lhs, expr)
                return Assign(lhs, expr)

            # not an assignment → force fallback
            raise ParseError("Not an assignment")

        except ParseError:
            self.pos = save_pos
            return self.parse_expression_statement()

    # --- Block ---
    def parse_block(self):
        stmts = []
        while self.current()[0] not in ("RBRACKET", None):
            stmts.append(self.parse_statement())
        if self.current()[0] == "RBRACKET":
            self.eat("RBRACKET")
        return stmts

    # --- Dispatcher ---
    def parse_statement(self):
        t = self.current()[0]

        if t == "PRINT":
            return self.parse_print_statement()
        if t == "INPUT":
            return self.parse_input_statement()
        if t == "IF":
            return self.parse_conditionals()
        if t == "FUN":
            return self.parse_function()
        if t == "IDENTIFIER":
            return self.parse_assignment_or_expr_statement()
        if t == "LPAREN":
            return self.parse_expression_statement()

        raise unexpected_token(self)
