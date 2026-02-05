from node import *
import interpreter.env as env

from runtime.builtins import builtins, BuiltinFunction

# Expression evaluation separated into its own module.
def evaluate(node):
    if isinstance(node, Number):
        return node.value

    elif isinstance(node, String):
        return node.value

    elif isinstance(node, Variable):
        if node.name in env.memory:     
            return env.memory[node.name]
        
        if node.name in builtins:
            return builtins[node.name]
        raise Exception(f"Undefined variable '{node.name}'")
        
    elif isinstance(node, ListAssign) and node.name is None:
        return [evaluate(item) for item in node.values]

    elif isinstance(node, ListAccessPos):
        if node.name not in env.memory:
            raise Exception(f"Undefined list '{node.name}'")
        lst = env.memory[node.name]
        index = evaluate(node.index)
        return lst[index]

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

        elif node.op == '&&':
            return left and right
        elif node.op == '||':
            return left or right

        else:
            raise Exception(f"Unknown operator '{node.op}'")

    elif isinstance(node, Input):
        if node.prompt:
            return input(node.prompt)
        return input()
    
    elif isinstance(node, FunctionCall):
        # Resolve function reference. `node.name` may be a ModuleAccess node
        # (for module/class member calls) or a plain identifier.
        if isinstance(node.name, ModuleAccess):
            func = evaluate(node.name)
        else:
            func = evaluate(Variable(node.name))

        args = [evaluate(arg) for arg in node.args]

        # Builtin functions
        if hasattr(func, "call"):
            return func.call(args)

        # User-defined function AST (Functions)
        if isinstance(func, Functions):
            if len(args) != len(func.params):
                raise Exception(
                    f"Function '{func.name}' expects {len(func.params)} arguments but got {len(args)}"
                )

            # execute function body in local memory
            old_memory = env.memory
            env.memory = {**env.memory, **dict(zip(func.params, args))}
            # import execute here to avoid circular imports at module import time
            from interpreter.executor import execute
            for s in func.body:
                execute(s)
            env.memory = old_memory
            return None

        raise Exception(f"'{getattr(node.name, 'name', node.name)}' is not callable")

    elif isinstance(node, ClassCall):
        classname = evaluate(Variable(node.name))
        functions = [evaluate(function) for function in node.functionName]

        if hasattr(classname, "call"):
            return classname.call(functions)
    

    elif isinstance(node, ModuleAccess):
        # First check imported modules
        if node.module_name in env.modules:
            module = env.modules[node.module_name]
            if node.member_name not in module:
                raise Exception(f"Module '{node.module_name}' has no member '{node.member_name}'")
            return module[node.member_name]

        # Then check locally defined classes
        if node.module_name in env.classes:
            classname = env.classes[node.module_name]
            for s in classname.body:
                if isinstance(s, Functions) and s.name == node.member_name:
                    return s
            raise Exception(f"Class '{node.module_name}' has no member '{node.member_name}'")

        raise Exception(f"Module or class '{node.module_name}' is not defined")  # Functions node or variable




    else:
        raise Exception(f"Cannot evaluate node: {node}")
