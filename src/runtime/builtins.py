class BuiltinFunction:
    def __init__(self, fn, arity=None):
        self.fn = fn
        self.arity = arity

    def call(self, args):
        if self.arity is not None and len(args) != self.arity:
            raise Exception("Wrong number of arguments")
        return self.fn(*args)


builtins = {}

# --------  MATH ---------------
import math 
import random

def b_abs(x):
    return abs(x)

def b_round(x, n):
    return round(x, n)

def b_sqrt(x):
    return math.sqrt(x)

def b_pow(x, y):
    return pow(x, y)

def b_max(*n):
    max(n)

def b_min(*n):
    min(n)

def b_randint(a, b):
    return random.randint(a, b)

def b_sin(x):
    return math.sin(x)

def b_cos(x):
    return math.cos(x)

def b_tan(x):
    return math.tan(x)

def b_asin(x):
    return math.asin(x)

def b_acos(x):
    return math.acos(x)

def b_atan(x):
    return math.atan(x)


builtins["abs"]  = BuiltinFunction(b_abs, 1)
builtins["round"]  = BuiltinFunction(b_round, 2)
builtins["sqrt"]  = BuiltinFunction(b_sqrt, 1)
builtins["pow"]  = BuiltinFunction(b_pow, 2)
builtins["max"]  = BuiltinFunction(b_max)
builtins["min"]  = BuiltinFunction(b_min)
builtins["randint"]  = BuiltinFunction(b_randint, 2)
builtins["sin"]  = BuiltinFunction(b_sin, 1)
builtins["cos"]  = BuiltinFunction(b_cos, 1)
builtins["tan"]  = BuiltinFunction(b_tan, 1)
builtins["asin"]  = BuiltinFunction(b_asin, 1)
builtins["acos"]  = BuiltinFunction(b_acos, 1)
builtins["atan"]  = BuiltinFunction(b_atan, 1)


# -------- String -----------


def b_len(value):
    return len(value)

def b_replace(value, old, new):
    return value.replace(old, new)

def b_split(value, separator):
    return value.split(separator)

builtins["ርዝመት"] = BuiltinFunction(b_len, 1)
builtins["ተካ"] = BuiltinFunction(b_replace, 3)
builtins["ክፈል"] = BuiltinFunction(b_split, 2)



# -------- FILE I/O BUILTINS --------

def b_open(path, mode):
    return open(path, mode)

def b_write(file_or_path, content):
    content = str(content)
    # If it's already a file object, just write
    if hasattr(file_or_path, "write"):
        file_or_path.write(content)
    # If it's a string path, open it and write
    else:
        with open(file_or_path, "w", encoding="utf-8") as f:
            f.write(content)
    return None

def b_read(file_or_path):
    if hasattr(file_or_path, "read"):
        return file_or_path.read()
    else:
        with open(file_or_path, "r", encoding="utf-8") as f:
            return f.read()

def b_close(file_or_path):
    if hasattr(file_or_path, "close"):
        file_or_path.close()
    return None



builtins["ክፈት"]  = BuiltinFunction(b_open, 2)
builtins["አንብብ"]  = BuiltinFunction(b_read, 1)
builtins["ጻፍ"] = BuiltinFunction(b_write, 2)
builtins["ዝጋ"] = BuiltinFunction(b_close, 1)
