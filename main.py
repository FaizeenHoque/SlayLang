from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

code = """
yap("hello" + " bestieeeee")
yap(2+2)
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
evaluator = Evaluator()
evaluator.evaluate(ast)