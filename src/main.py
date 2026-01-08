# main.py

import argparse
import os
from lexer import tokenize
from parser import Parser
from interpreter.interpreter import run

# -------------------------------
# Argument parsing
# -------------------------------
parser = argparse.ArgumentParser(description="Abyssinia Lang Interpreter")
parser.add_argument('-f', '--file', type=str, help='Path to .aby file to run')
args = parser.parse_args()

if args.file:
    # Get absolute path to the .aby file
    aby_file = os.path.abspath(args.file)
    
    # Change working directory to the .aby file's folder
    aby_dir = os.path.dirname(aby_file)
    os.chdir(aby_dir)

    # Read source code
    with open(aby_file, "r", encoding="utf-8-sig") as f:
        code = f.read()
else:
    print("Interpreter for AbyssLang programming language, made by Tsegab")
    code = input(">>> ")

# -------------------------------
# Tokenize, parse, run
# -------------------------------
tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

run(ast)
