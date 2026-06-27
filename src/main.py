"""Simple entry point that loads and runs the sample SlayLang file.

This file is a tiny helper for trying the language from inside the source tree.
It reads the example program, parses it, and then runs it.
"""

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

with open('../program.slay', 'r') as file:
    code = file.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
evaluator = Evaluator()
evaluator.evaluate(ast)