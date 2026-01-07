# parser.py
from node import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --- Token Helpers ---
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def peek_next(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1][0]
        return None

    def eat(self, token_type):
        type_, value = self.current()
        if type_ == token_type:
            self.pos += 1
            return value
        raise Exception(f"Expected {token_type} but got {type_} (value={value!r}) at pos={self.pos}")

    # --- Expressions ---
    def parse_num_or_var(self):
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
            if self.current()[0] == "LPAREN":
                return self.parse_function_call(name)
            return Variable(name)
        if type_ == "LPAREN":
            return self.parse_parens(self.parse_logical)
        raise Exception(f"Unexpected token {type_} (value={value!r}) at pos={self.pos}")

    def parse_parens(self, parse_fn):
        self.eat("LPAREN")
        node = parse_fn()
        self.eat("RPAREN")
        return node

    def parse_function_call(self, name):
        self.eat("LPAREN")
        args = []
        if self.current()[0] != "RPAREN":
            while True:
                args.append(self.parse_expression())
                if self.current()[0] == "COMMA":
                    self.eat("COMMA")
                    if self.current()[0] == "RPAREN": break
                    continue
                break
        self.eat("RPAREN")
        return FunctionCall(name, args)

    # --- Operator Precedence ---
    def parse_term(self):
        left = self.parse_num_or_var()
        while self.current()[0] in ("MULT", "DIV"):
            op = self.eat(self.current()[0])
            right = self.parse_num_or_var()
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

    # --- Statements ---
    def parse_expression_statement(self):
        stmt_start_tokens = {"PRINT", "IF", "FUN", "ELSE", "ELSEIF", "LBRACKET", "RBRACKET"}
        if self.current()[0] in stmt_start_tokens:
            raise Exception(f"parse_expression_statement called on {self.current()[0]} at pos={self.pos}")
        expr = self.parse_logical()
        self.eat("SEMICOLON")
        return expr

    def parse_print_statement(self):
        self.eat("PRINT")
        expr = self.parse_parens(self.parse_logical)
        self.eat("SEMICOLON")
        return Print(expr)

    def parse_assignment_or_expr_statement(self):
        name = self.eat("IDENTIFIER")
        if self.current()[0] == "EQUAL":
            self.eat("EQUAL")
            expr = self.parse_logical()
            self.eat("SEMICOLON")
            return Assign(name, expr)
        else:
            self.pos -= 1
            return self.parse_expression_statement()

    def parse_statement(self):
        type_ = self.current()[0]
        if type_ == "PRINT": return self.parse_print_statement()
        if type_ == "INPUT": return self.parse_input_statement()
        if type_ == "IF": return self.parse_conditionals()
        if type_ == "FUN": return self.parse_function()
        if type_ == "IDENTIFIER": return self.parse_assignment_or_expr_statement()
        if type_ == "LPAREN": return self.parse_expression_statement()
        raise Exception(f"Unknown statement starting with {type_} at pos={self.pos}")
    
    # --- Inputs ---
    def parse_input_statement(self):
        self.eat("INPUT")
        prompt = None
        # Optional prompt string in parentheses
        if self.current()[0] == "LPAREN":
            self.eat("LPAREN")
            if self.current()[0] == "STRING":
                prompt = self.eat("STRING")
            self.eat("RPAREN")
        self.eat("SEMICOLON")
        return Input(prompt)


    # --- Blocks ---
    def parse_block(self):
        stmts = []
        while self.current()[0] not in ("RBRACKET", None):
            stmts.append(self.parse_statement())
        if self.current()[0] == "RBRACKET":
            self.eat("RBRACKET")
        return stmts

    # --- Conditionals ---
    def parse_conditionals(self):
        self.eat("IF")
        condition = self.parse_parens(self.parse_logical)
        self.eat("LBRACKET")
        body = self.parse_block()

        elseif_cond, elseif_body = None, None
        if self.current()[0] == "ELSEIF":
            self.eat("ELSEIF")
            elseif_cond = self.parse_parens(self.parse_logical)
            self.eat("LBRACKET")
            elseif_body = self.parse_block()

        else_body = None
        if self.current()[0] == "ELSE":
            self.eat("ELSE")
            self.eat("LBRACKET")
            else_body = self.parse_block()

        return Conditionals(condition, body, elseif_cond, elseif_body, else_body)

    # --- Functions ---
    def parse_function(self):
        self.eat("FUN")
        func_name = self.eat("IDENTIFIER")
        params = self.parse_param_list()
        self.eat("LBRACKET")
        body = self.parse_block()
        return Functions(func_name, params, body)

    def parse_param_list(self):
        params = []
        self.eat("LPAREN")
        while self.current()[0] != "RPAREN":
            params.append(self.eat("IDENTIFIER"))
            if self.current()[0] == "COMMA":
                self.eat("COMMA")
        self.eat("RPAREN")
        return params

    # --- Entry Point ---
    def parse(self):
        stmts = []
        while self.current()[0] is not None:
            stmts.append(self.parse_statement())
        return stmts
