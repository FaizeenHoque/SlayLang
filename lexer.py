KEYWORDS = {
    "facts": "TRUE",
    "cap": "FALSE",
    "ghosted": "NULL",

    "vibe": "LET",
    "lock": "CONST",

    "sus": "IF",
    "mid": "ELSE_IF",
    "tho": "ELSE",

    "grind": "WHILE",
    "spin": "FOR",
    "roam": "FOR_OF",

    "dip": "BREAK",
    "skip": "CONTINUE",

    "cook": "FUNCTION",
    "yeet": "RETURN",

    "fw": "IMPORT",

    "no_shot": "TRY",
    "ratio": "CATCH",
    "flop": "THROW",

    "ghost": "DELETE",
}
BUILTINS = {
    "yap": "PRINT",
    "spill": "PRINT_LOUD",
    "interrogate": "INPUT",
}
OPERATORS = {
    "=>": "ARROW",

    "&&": "AND",
    "||": "OR",
    "nah": "NOT",

    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    "%": "MODULO",
    "**": "POWER",

    "=": "ASSIGN",

    "+=": "ADD_ASSIGN",
    "-=": "SUB_ASSIGN",
    "*=": "MUL_ASSIGN",
    "/=": "DIV_ASSIGN",

    "==": "EQUAL",
    "!=": "NOT_EQUAL",
    ">": "GT",
    "<": "LT",
    ">=": "GT_EQUAL",
    "<=": "LT_EQUAL",
}
PUNCTUATION = {
    "(": "LPAREN",
    ")": "RPAREN",

    "[": "LBRACKET",
    "]": "RBRACKET",

    "{": "LBRACE",
    "}": "RBRACE",

    ",": "COMMA",
    ":": "COLON",
    ".": "DOT",
}

class Token():
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type}, {self.value!r})"


class Lexer:
    def __init__(self, source: str):
        self.source = source

        if self.source == '':
            raise Exception("bestie.. you gave nothing to lex 💀")

        self.index = 0
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
                tokens.append(Token("NEWLINE", '\n'))
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
                    raise Exception("bestie... '/' operator not implemented yet 💀") 

            elif (self.current_character in OPERATORS or (self.peek() is not None and (self.current_character + self.peek()) in OPERATORS)):
                tokens.append(self.read_operator()) 

            elif self.current_character in PUNCTUATION:
                tokens.append(Token(PUNCTUATION.get(self.current_character), self.current_character))
                self.advance()

            else:
                raise Exception(f"bestie... '{self.current_character}' is not valid 💀")

        tokens.append(Token("EOF", None))
        return tokens

    def read_string(self, opening_quote):
        output = ""

        while self.current_character != opening_quote:
            if self.current_character is None:
                raise Exception("unterminated string")

            output += self.current_character
            self.advance()

        self.advance()
        return Token("STRING", output)

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
            return Token("NUMBER", float(number_value))
        else:
            return Token("NUMBER", int(number_value))

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
            token_type = "IDENT"

        return Token(token_type, word_value)

    def skip_comment(self):
        self.advance() 

        if self.current_character == "/":
            self.advance() 

            while self.current_character is not None and self.current_character != "\n":
                self.advance()

            if self.current_character == "\n":
                self.advance()
    
    def read_operator(self):
        current = self.current_character
        next_char = self.peek()

        if next_char is not None and (current + next_char) in OPERATORS:
            op = current + next_char
            self.advance()
            self.advance()

            return Token(OPERATORS[op], op)
        
        if current in OPERATORS:
            op = current
            self.advance()
            return Token(OPERATORS[op], op)
        
        raise Exception(f"dawg.. what operator is {current}??")

    def peek(self):
        if self.index + 1 >= len(self.source):
            return None
        return self.source[self.index + 1]


if __name__ == "__main__":
    lexer = Lexer("vibe x = 123 + 45.6 // comment\nyap(x)")
    tokens = lexer.tokenize()
    print(tokens)