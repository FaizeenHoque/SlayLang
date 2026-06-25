from lexer import Lexer

with open("./test.slay", "r", encoding="utf-8") as file:
    text = file.read()

lexer = Lexer(text)
tokens = lexer.tokenize()
print(tokens)
