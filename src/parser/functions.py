# parser/functions.py
from node import *

class FunctionParser:
    def parse_function(self):
        self.eat("FUN")
        name = self.eat("IDENTIFIER")
        params = self.parse_param_list()
        self.eat("LBRACKET")
        body = self.parse_block()
        return Functions(name, params, body)

    def parse_param_list(self):
        params = []
        self.eat("LPAREN")
        if self.current()[0] != "RPAREN":
            while True:
                params.append(self.eat("IDENTIFIER"))
                if self.current()[0] == "COMMA":
                    self.eat("COMMA")
                    continue
                break
        self.eat("RPAREN")
        return params

    def parse_function_call(self, name):
        self.eat("LPAREN")
        args = []
        if self.current()[0] != "RPAREN":
            while True:
                args.append(self.parse_expression())
                if self.current()[0] == "COMMA":
                    self.eat("COMMA")
                    continue
                break
        self.eat("RPAREN")
        return FunctionCall(name, args)
