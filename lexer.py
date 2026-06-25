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
    def __init__(self, type: str, value:any):
        self.type = type
        self.value = value
    def __repr__(self):
        if isinstance(self.value, str):
            return f"{self.__class__.__name__}({self.type}, '{self.value!r}')"
        else:
            return f"{self.__class__.__name__}({self.type}, {self.value!r})"

class Lexer:
    def __init__(self, source:str):
        self.source = source

        if (self.source == ''):
            raise Exception("bestie.. you gave nothing to lex 💀") 
        
        self.index = 0
        self.current_character = self.source[self.index]
    def advance(self):
        self.index += 1
        if (self.index >= len(self.source)):
            self.current_character = None
        else:
            self.current_character = self.source[self.index]
    def tokenize(self):
        tokens = []
        while self.current_character is not None:
            if (self.current_character == ' '):
                self.advance()
            elif (self.current_character == '\n'):
                tokens.append(Token("NEWLINE", '\n'))
                self.advance()
            elif (self.current_character in PUNCTUATION):
                tokens.append(Token(PUNCTUATION.get(self.current_character), self.current_character))
                self.advance()
            elif (self.current_character == '"' or self.current_character == "'"):
                self.advance()
                tokens.append(self.read_string(self.source[self.index-1]))
            else:
                raise Exception(f"bestie... '{self.current_character}' is not valid 💀")
        
        tokens.append(Token("EOF", None))
        return tokens

    def read_string(self, opening_quote):
        string_value = ""

        while self.current_character != opening_quote:
            if self.current_character == None:
                raise Exception("unterminated string")

            string_value += self.current_character
            self.advance()

        self.advance()
        return Token("STRING", string_value)

if __name__ == "__main__":
    lexer = Lexer("'wtf'\n")
    tokens = lexer.tokenize()
    print(tokens)