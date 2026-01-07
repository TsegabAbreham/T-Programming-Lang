# parser/control.py
from node import *

class ControlParser:
    def parse_conditionals(self):
        self.eat("IF")
        condition = self.parse_parens(self.parse_logical)
        self.eat("LBRACKET")
        body = self.parse_block()

        elseif_cond = elseif_body = None
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
