from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

with open('./program.slay', 'r') as file:
    code = file.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
evaluator = Evaluator()
evaluator.evaluate(ast)