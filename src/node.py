
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

# --- List Variables ---
class ListAssign:
    def __init__(self, name, values):
        self.name = name
        self.values = values

class ListAccessPos:
    def __init__(self, name, index):
        self.name = name
        self.index = index

class AssignListElement:
    def __init__(self, list_access, value):
        self.list_access = list_access  # ListAccess node
        self.value = value              # expression node

# --- Keywords ---
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

# --- Functions ---
class Functions:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Input:
    def __init__(self, prompt=None):
        self.prompt = prompt

# --- Loops ---
class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoop:
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

# --- Imports ---
class ImportStatement:
    def __init__(self, path, alias=None):
        self.path = path
        self.alias = alias

class ModuleAccess:
    def __init__(self, module_name, member_name):
        self.module_name = module_name
        self.member_name = member_name

# --- Classes ---
class Classes:
    def __init__(self, name, body):
        self.name = name
        self.body = body

class ClassCall:
    def __init__(self, name, functionName):
        self.name = name
        self.functionName = functionName