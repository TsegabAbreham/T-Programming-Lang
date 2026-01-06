
class Number:
    def __init__(self, value):
        self.value = value

class String:
    def __init__(self, value):
        self.value = value

class Variable:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Print:
    def __init__(self, expr):
        self.expr = expr

class Conditionals:
    def __init__(self, condition, body, elseif_condition=None, elseif_body=None, else_body=None):
        self.condition = condition
        self.body = body
        self.elseif_condition = elseif_condition
        self.elseif_body = elseif_body
        self.else_body = else_body

class Functions:
    def __init__(self, value, params, body):
        self.value = value
        self.params = params
        self.body = body
class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args