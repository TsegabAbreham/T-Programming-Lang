from node import *

class ClassParser:
    def parse_class(self):
        self.eat("CLASS")
        name = self.eat("IDENTIFIER")
        self.eat("LBRACKET")
        # class body can contain multiple statements (usually function definitions)
        body = self.parse_block()
        return Classes(name, body)
    
    def parse_class_call(self, name, functionName):
        self.eat("DOT")
        functionName = self.parse_function_call()
        return ClassCall(name, functionName)
