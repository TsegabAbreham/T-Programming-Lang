from node import *

# memory storage
memory = {}

def evaluate(node):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, String):
        return node.value
    elif isinstance(node, Variable):
        return memory[node.name]
    elif isinstance(node, BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        elif node.op == '>':
            return left > right
        elif node.op == '<':
            return left < right
        elif node.op == '>=':
            return left >= right
        elif node.op == '<=':
            return left <= right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        else:
            raise Exception(f"Unknown operator: {node.op}")
    else:
        raise Exception(f"Cannot evaluate node: {node}")


def run(ast):
    for stmt in ast:
        execute(stmt)

def execute(stmt):
    if isinstance(stmt, Assign):
        memory[stmt.name] = evaluate(stmt.value)
    elif isinstance(stmt, Print):
        print(evaluate(stmt.expr))
    elif isinstance(stmt, Conditionals):
        # IF
        if evaluate(stmt.condition):
            for s in stmt.body:
                execute(s)
        # ELSEIF
        elif stmt.elseif_condition is not None and evaluate(stmt.elseif_condition):
            for s in stmt.elseif_body:
                execute(s)
        # ELSE
        elif stmt.else_body is not None:
            for s in stmt.else_body:
                execute(s)
