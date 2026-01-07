# parser/lists.py
from node import *

class ListParser:
    def parse_list(self):
        self.eat("SLBRACKET")
        elements = []

        if self.current()[0] == "SRBRACKET":
            self.eat("SRBRACKET")
            return elements

        while True:
            elements.append(self.parse_logical())
            if self.current()[0] == "COMMA":
                self.eat("COMMA")
                continue
            break

        self.eat("SRBRACKET")
        return elements
