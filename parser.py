from node import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)
    
    def eat(self, token_type):
        type_, value = self.current()
        if type_ == token_type:
            self.pos += 1
            return value
        raise Exception(f"Expected {token_type} but got {type_}")

    # --- Basic elements ---
    def parse_num_or_var(self):
        type_, value = self.current()
        if type_ == "NUMBER":
            self.eat("NUMBER")
            return Number(int(value))
        elif type_ == "STRING":
            self.eat("STRING")
            return String(value)
        elif type_ == "IDENTIFIER":
            name = self.eat("IDENTIFIER")

             # function call
            if self.current()[0] == "LPAREN":
                self.eat("LPAREN")
                args = []

                if self.current()[0] != "RPAREN":
                    args.append(self.parse_expression())
                    while self.current()[0] == "COMMA":
                        self.eat("COMMA")
                        args.append(self.parse_expression())

                self.eat("RPAREN")
                return FunctionCall(name, args)

            # normal variable
            return Variable(name)
        


        elif type_ == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_comparison()
            self.eat("RPAREN")
            return node
        else:
            raise Exception("Expected number, string, or variable")

    def parse_term(self):
        left = self.parse_num_or_var()
        while True:
            type_, value = self.current()
            if type_ in ("MULT", "DIV"):
                self.eat(type_)
                right = self.parse_num_or_var()
                left = BinOp(left, value, right)
            else:
                break
        return left

    def parse_expression(self):
        left = self.parse_term()
        while True:
            type_, value = self.current()
            if type_ in ("PLUS", "MINUS"):
                self.eat(type_)
                right = self.parse_term()
                left = BinOp(left, value, right)
            else:
                break
        return left

    def parse_comparison(self):
        left = self.parse_expression()
        type_, value = self.current()
        if type_ in ("EQ", "NEQ", "GT", "LT", "GTE", "LTE"):
            self.eat(type_)
            right = self.parse_expression()
            left = BinOp(left, value, right)
        return left

    # --- Statements ---
    def parse_expression_statement(self):
        expr = self.parse_comparison()
        if self.current()[0] == "SEMICOLON":
            self.eat("SEMICOLON")
        else:
            raise Exception("Missing semicolon after expression")
        return expr

    def parse_statement(self):
        type_, _ = self.current()


        if type_ == "IF":
            return self.parse_conditionals()
        elif type_ == "FUN":
            return self.parse_function()
        elif type_ == "PRINT" or (type_ == "IDENTIFIER" and self.peek_next() == "LPAREN"):
            self.eat(type_)  # consume PRINT or IDENTIFIER (function call)
            self.eat("LPAREN")
            expr = self.parse_comparison()
            self.eat("RPAREN")
            if self.current()[0] == "SEMICOLON":
                self.eat("SEMICOLON")
            else:
                raise Exception("Missing semicolon after print statement")
            return Print(expr)

        elif type_ == "IDENTIFIER":
            # check if assignment
            if self.peek_next() == "EQUAL":
                var_name = self.eat("IDENTIFIER")
                self.eat("EQUAL")
                expr = self.parse_comparison()
                if self.current()[0] == "SEMICOLON":
                    self.eat("SEMICOLON")
                else:
                    raise Exception(f"Missing semicolon after assignment to {var_name}")
                return Assign(var_name, expr)
            else:
                # standalone expression
                return self.parse_expression_statement()

        elif type_ == "LPAREN":
            return self.parse_expression_statement()

        else:
            raise Exception(f"Unknown statement starting with {type_}")

    def peek_next(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1][0]
        return None

    # --- Blocks ---
    def parse_block(self):
        statements = []
        while True:
            type_, _ = self.current()
            if type_ == "RBRACKET" or type_ is None:
                if type_ == "RBRACKET":
                    self.eat("RBRACKET")
                break
            statements.append(self.parse_statement())
        return statements

    # --- Conditionals ---
    def parse_conditionals(self):
        self.eat("IF")
        self.eat("LPAREN")
        condition = self.parse_comparison()
        self.eat("RPAREN")

        if self.current()[0] != "LBRACKET":
            raise Exception("Missing opening bracket for IF block")
        self.eat("LBRACKET")
        body = self.parse_block()

        # ELSEIF
        elseif_condition = None
        elseif_body = None
        if self.current()[0] == "ELSEIF":
            self.eat("ELSEIF")
            self.eat("LPAREN")
            elseif_condition = self.parse_comparison()
            self.eat("RPAREN")
            if self.current()[0] != "LBRACKET":
                raise Exception("Missing opening bracket for ELSEIF block")
            self.eat("LBRACKET")
            elseif_body = self.parse_block()

        # ELSE
        else_body = None
        if self.current()[0] == "ELSE":
            self.eat("ELSE")
            if self.current()[0] != "LBRACKET":
                raise Exception("Missing opening bracket for ELSE block")
            self.eat("LBRACKET")
            else_body = self.parse_block()

        return Conditionals(condition, body, elseif_condition, elseif_body, else_body)
    
    # --- Functions ---
    def parse_function(self):
        # fun myFunc() { ... }
        self.eat("FUN")

        # function name
        if self.current()[0] != "IDENTIFIER":
            raise Exception("Expected function name after 'fun'")
        func_name = self.eat("IDENTIFIER")

        # parameters
        self.eat("LPAREN")

        params = []
        if self.current()[0] != "RPAREN":
            while True:
                if self.current()[0] != "IDENTIFIER":
                    raise Exception("Expected parameter name")
                params.append(self.eat("IDENTIFIER"))

                if self.current()[0] == "COMMA":
                    self.eat("COMMA")
                else:
                    break

        self.eat("RPAREN")

        # function body
        if self.current()[0] != "LBRACKET":
            raise Exception("Missing opening '{' for function body")
        self.eat("LBRACKET")

        body = self.parse_block()

        return Functions(func_name, params, body)

    # --- Entry point ---
    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.parse_statement())
        return statements
