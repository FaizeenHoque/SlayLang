# lexer.py

from tokens import *


class Token():
    def __init__(self, type: str, value: any, line: int = 0):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type}, {self.value!r})"


class Lexer:
    def __init__(self, source: str):
        self.source = source

        if self.source == '':
            raise Exception("bestie.. you gave nothing to lex 💀")

        self.index = 0
        self.line = 1
        self.current_character = self.source[self.index]

    def advance(self):
        self.index += 1
        if self.index >= len(self.source):
            self.current_character = None
        else:
            self.current_character = self.source[self.index]

    def tokenize(self):
        tokens = []

        while self.current_character is not None:
            if self.current_character == ' ':
                self.advance()

            elif self.current_character == '\n':
                tokens.append(Token(TokenType.NEWLINE, '\n', self.line))
                self.line += 1
                self.advance()

            elif self.current_character == '"' or self.current_character == "'":
                opening_quote = self.current_character  
                self.advance()
                tokens.append(self.read_string(opening_quote))

            elif self.current_character.isdigit():
                tokens.append(self.read_number())

            elif self.current_character.isalpha() or self.current_character == "_":
                tokens.append(self.read_word())

            elif self.current_character == "/":
                if self.peek() == "/":
                    self.skip_comment()
                else:
                    tokens.append(self.read_operator())

            elif (self.current_character in OPERATORS or (self.peek() is not None and (self.current_character + self.peek()) in OPERATORS)):
                tokens.append(self.read_operator()) 

            elif self.current_character in PUNCTUATION:
                tokens.append(Token(PUNCTUATION.get(self.current_character), self.current_character, self.line))
                self.advance()

            else:
                raise Exception(f"bestie... '{self.current_character}' is not valid 💀")

        tokens.append(Token(TokenType.EOF, None, self.line))
        return tokens

    def read_string(self, opening_quote):
        output = ""

        while self.current_character != opening_quote:
            if self.current_character is None:
                raise Exception("unterminated string")

            output += self.current_character
            self.advance()

        self.advance()  # consume closing quote
        return Token(TokenType.STRING, output, self.line)

    def read_number(self):
        number_value = ""
        dot_count = 0

        while self.current_character is not None:
            if self.current_character.isdigit():
                number_value += self.current_character

            elif self.current_character == ".":
                dot_count += 1
                if dot_count > 1:
                    break
                number_value += self.current_character

            else:
                break

            self.advance()

        if "." in number_value:
            return Token(TokenType.NUMBER, float(number_value), self.line)
        else:
            return Token(TokenType.NUMBER, int(number_value), self.line)

    def read_word(self):
        word_value = ""

        while self.current_character is not None and (
            self.current_character.isalnum() or self.current_character == "_"
        ):
            word_value += self.current_character
            self.advance()

        if word_value in KEYWORDS:
            token_type = KEYWORDS[word_value]
        elif word_value in BUILTINS:
            token_type = BUILTINS[word_value]
        elif word_value in OPERATORS:
            token_type = OPERATORS[word_value]
        else:
            token_type = TokenType.IDENT

        return Token(token_type, word_value, self.line)

    def skip_comment(self):
        self.advance()  # consume first '/'

        if self.current_character == "/":
            self.advance()  # consume second '/'

            while self.current_character is not None and self.current_character != "\n":
                self.advance()

            if self.current_character == "\n":
                self.line += 1
                self.advance()  # consume the newline

    def read_operator(self):
        current = self.current_character
        next_char = self.peek()

        if next_char is not None and (current + next_char) in OPERATORS:
            op = current + next_char
            self.advance()
            self.advance()
            return Token(OPERATORS[op], op, self.line)
        
        if current in OPERATORS:
            op = current
            self.advance()
            return Token(OPERATORS[op], op, self.line)
        
        raise Exception(f"dawg.. what operator is {current}??")

    def peek(self):
        if self.index + 1 >= len(self.source):
            return None
        return self.source[self.index + 1]


if __name__ == "__main__":
    lexer = Lexer("vibe x = 123 + 45.6 // comment\nyap(x)")
    tokens = lexer.tokenize()
    print(tokens)