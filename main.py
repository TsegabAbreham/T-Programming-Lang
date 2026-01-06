# main.py

import argparse

from lexer import tokenize
from parser import Parser
from interpreter import run

parser = argparse.ArgumentParser(description="Tsegab Programming Language Interpreter")
parser.add_argument('-f', '--file', type=str, help='File path to run')

args = parser.parse_args()

if args.file:
    with open(args.file, 'r') as f:
        code = f.read()
else:
    print("Interpreter for T programming language, made by Tsegab")
    code = input(">>> ")

tokens = tokenize(code)
parser = Parser(tokens)
ast = parser.parse()

run(ast)