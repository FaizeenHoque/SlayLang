from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

code = """
cook add(a, b) {
    yeet a + b
}

vibe a = numify(snoop("first number: "))
vibe b = numify(snoop("second number: "))

yap("answer:", add(a, b))
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
evaluator = Evaluator()
evaluator.evaluate(ast)