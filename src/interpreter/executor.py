from node import *
import interpreter.env as env
from interpreter.evaluator import evaluate

# Statement execution and program run separated into executor.
def execute(stmt):
    # Variable assignment
    if isinstance(stmt, Assign):
        env.memory[stmt.name] = evaluate(stmt.value)

    # List assignment: test = [1,2,3]
    elif isinstance(stmt, ListAssign):
        env.memory[stmt.name] = [evaluate(item) for item in stmt.values]

    # List element assignment: test[0] = 10
    elif isinstance(stmt, AssignListElement):
        list_name = stmt.list_access.name
        index = evaluate(stmt.list_access.index)
        value = evaluate(stmt.value)

        if list_name not in env.memory:
            raise Exception(f"Undefined list '{list_name}'")

        env.memory[list_name][index] = value

    # Print
    elif isinstance(stmt, Print):
        print(evaluate(stmt.expr))

    # Input as statement
    elif isinstance(stmt, Input):
        if stmt.prompt:
            return input(stmt.prompt)
        return input()

    # Conditionals
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
    
    # Loops
    elif isinstance(stmt, WhileLoop):
        while evaluate(stmt.condition):
            for s in stmt.body:
                execute(s)
    
    elif isinstance(stmt, ForLoop):
        start = evaluate(stmt.start)
        end = evaluate(stmt.end)

        for i in range(start, end):
            env.memory[stmt.var] = i
            for s in stmt.body:
                execute(s)
                
    # Function definition
    elif isinstance(stmt, Functions):
        env.functions[stmt.name] = stmt

    # Function call
    elif isinstance(stmt, FunctionCall):
        # Check if it's a user-defined function first
        if stmt.name in env.functions:
            func = env.functions[stmt.name]

            if len(stmt.args) != len(func.params):
                raise Exception(
                    f"Function '{stmt.name}' expects {len(func.params)} arguments "
                    f"but got {len(stmt.args)}"
                )

            # Evaluate arguments
            arg_values = [evaluate(arg) for arg in stmt.args]

            # Create local scope for the call
            old_memory = env.memory
            env.memory = {**env.memory, **dict(zip(func.params, arg_values))}

            # Execute the function body
            for s in func.body:
                execute(s)

            # Restore previous memory
            env.memory = old_memory

        else:
            # If it's not a user function, treat it as an expression (built-in)
            evaluate(stmt)

    # expression statements
    elif isinstance(stmt, (ListAccessPos, BinOp, Variable, Number, String)):
        evaluate(stmt)

    else:
        raise Exception(f"Unknown statement type: {stmt}")


def run(ast):
    for stmt in ast:
        execute(stmt)
