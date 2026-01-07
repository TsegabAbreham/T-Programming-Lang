from node import *

# memory storage
memory = {}
functions = {}

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
        elif node.op == "&&":
            return left and right
        elif node.op == "||":
            return left or right
        else:
            raise Exception(f"Unknown operator: {node.op}")
    elif isinstance(node, Input):
        if node.prompt:
            return input(node.prompt)
        else:
            return input()

    else:
        raise Exception(f"Cannot evaluate node: {node}")


def run(ast):
    for stmt in ast:
        execute(stmt)

def execute(stmt):
    global memory
    
    if isinstance(stmt, Assign):
        memory[stmt.name] = evaluate(stmt.value)

    elif isinstance(stmt, Print):
        print(evaluate(stmt.expr))
    
    elif isinstance(stmt, Input):
        if stmt.prompt:
            return input(stmt.prompt)
        else:
            return input()

    elif isinstance(stmt, Conditionals):
        if evaluate(stmt.condition):
            for s in stmt.body:
                execute(s)
        elif stmt.elseif_condition is not None and evaluate(stmt.elseif_condition):
            for s in stmt.elseif_body:
                execute(s)
        elif stmt.else_body is not None:
            for s in stmt.else_body:
                execute(s)

    elif isinstance(stmt, Functions):
        # store the function in the functions table
        functions[stmt.name] = stmt

    elif isinstance(stmt, FunctionCall):
        if stmt.name not in functions:
            raise Exception(f"Function '{stmt.name}' is not defined")
        func_def = functions[stmt.name]

        if len(stmt.args) != len(func_def.params):
            raise Exception(f"Function '{stmt.name}' expects {len(func_def.params)} arguments but got {len(stmt.args)}")

        # Evaluate arguments
        arg_values = [evaluate(arg) for arg in stmt.args]

        # create a local memory for this function call
        local_memory = dict(zip(func_def.params, arg_values))

        # Save current memory and switch to local scope
        
        old_memory = memory
        memory = {**memory, **local_memory}  # combine global + local

        # Execute function body
        for s in func_def.body:
            execute(s)

        # restore old memory
        memory = old_memory

    else:
        raise Exception(f"Unknown statement type: {stmt}")

