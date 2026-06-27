"""Define the token names and shared token groups used by the SlayLang lexer and parser.

This file acts like the language's symbol list. It gives names to every kind of
word, number, operator, and punctuation mark that the lexer can produce and the
parser can understand.
"""

from enum import Enum


class TokenType(Enum):
    """Name every kind of token that SlayLang knows how to read."""

    # Control flow
    IF          = "IF"
    ELSE_IF     = "ELSE_IF"
    ELSE        = "ELSE"
    WHILE       = "WHILE"
    FOR         = "FOR"
    # FOR_OF      = "FOR_OF"
    BREAK       = "BREAK"
    CONTINUE    = "CONTINUE"
    RETURN      = "RETURN"
    FUNCTION    = "FUNCTION"

    # Variable declarations & assignment
    LET         = "LET"
    CONST       = "CONST"
    ASSIGN      = "ASSIGN"
    ADD_ASSIGN  = "ADD_ASSIGN"
    SUB_ASSIGN  = "SUB_ASSIGN"
    MUL_ASSIGN  = "MUL_ASSIGN"
    DIV_ASSIGN  = "DIV_ASSIGN"

    # Literals
    NUMBER      = "NUMBER"
    STRING      = "STRING"
    TRUE        = "TRUE"
    FALSE       = "FALSE"
    NULL        = "NULL"

    # Identifiers & structure
    IDENT       = "IDENT"
    EOF         = "EOF"
    NEWLINE     = "NEWLINE"

    # Arithmetic operators
    PLUS        = "PLUS"
    MINUS       = "MINUS"
    MULTIPLY    = "MULTIPLY"
    DIVIDE      = "DIVIDE"
    FLOOR_DIVIDE= "FLOOR_DIVIDE"
    MODULO      = "MODULO"
    POWER       = "POWER"

    # List operations
    LEN         = "LEN"
    PUSH        = "PUSH"
    POP         = "POP"

    # Comparison operators
    EQUAL       = "EQUAL"
    NOT_EQUAL   = "NOT_EQUAL"
    GT          = "GT"
    LT          = "LT"
    GT_EQUAL    = "GT_EQUAL"
    LT_EQUAL    = "LT_EQUAL"

    # Logical operators
    AND         = "AND"
    OR          = "OR"
    NOT         = "NOT"

    # Built-in functions
    PRINT       = "PRINT"
    PRINT_LOUD  = "PRINT_LOUD"
    FLOATIFY    = "FLOATIFY"
    INTIFY      = "INTIFY"
    INPUT       = "INPUT"

    # Punctuation / delimiters
    LPAREN      = "LPAREN"
    RPAREN      = "RPAREN"
    LBRACKET    = "LBRACKET"
    RBRACKET    = "RBRACKET"   
    LBRACE      = "LBRACE"
    RBRACE      = "RBRACE"
    COMMA       = "COMMA"
    COLON       = "COLON"
    SEMI_COLON  = "SEMI_COLON"            
    DOT         = "DOT"        

    # Miscellaneous
    ARROW       = "ARROW"
    DELETE      = "DELETE"
    IMPORT      = "IMPORT"
    TRY         = "TRY"
    CATCH       = "CATCH"
    THROW       = "THROW"

INBUILT_FUNCTIONS = {TokenType.PRINT, TokenType.PRINT_LOUD, TokenType.INPUT, TokenType.INTIFY, TokenType.FLOATIFY, TokenType.LEN, TokenType.PUSH, TokenType.POP}

BOOLEANS = {TokenType.TRUE, TokenType.FALSE}

BINARY_OPERATORS = {
    TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
    TokenType.DIVIDE, TokenType.MODULO, TokenType.POWER,
    TokenType.EQUAL, TokenType.NOT_EQUAL,
    TokenType.GT, TokenType.LT, TokenType.GT_EQUAL, TokenType.LT_EQUAL, TokenType.FLOOR_DIVIDE
}

KEYWORDS = {
    "nocap":    TokenType.TRUE,
    "cap":      TokenType.FALSE,
    "ghosted":  TokenType.NULL,
    "vibe":     TokenType.LET,
    "lockedin": TokenType.CONST,
    "sus":      TokenType.IF,
    "mid":      TokenType.ELSE_IF,
    "tho":      TokenType.ELSE,
    "grind":    TokenType.WHILE,
    "spin":     TokenType.FOR,
    # "roam":     TokenType.FOR_OF,
    "dip":      TokenType.BREAK,
    "skip":     TokenType.CONTINUE,
    "cook":     TokenType.FUNCTION,
    "yeet":     TokenType.RETURN,
    # "fw":       TokenType.IMPORT,
    # "nochance": TokenType.TRY,
    # "ratiod":   TokenType.CATCH,
    # "flop":     TokenType.THROW,
    # "poof":     TokenType.DELETE,
}

BUILTINS = {
    "yap":   TokenType.PRINT,
    "rant":  TokenType.PRINT_LOUD,
    "snoop": TokenType.INPUT,
    "floatify": TokenType.FLOATIFY,
    "intify": TokenType.INTIFY,
    "len": TokenType.LEN,
    "push": TokenType.PUSH,
    "pop": TokenType.POP
}

OPERATORS = {
    "=>": TokenType.ARROW,
    "&&": TokenType.AND,
    "||": TokenType.OR,
    "nah": TokenType.NOT,
    "+":  TokenType.PLUS,
    "-":  TokenType.MINUS,
    "*":  TokenType.MULTIPLY,
    "/":  TokenType.DIVIDE,
    "\\":  TokenType.FLOOR_DIVIDE,
    "%":  TokenType.MODULO,
    "**": TokenType.POWER,
    "=":  TokenType.ASSIGN,
    "+=": TokenType.ADD_ASSIGN,
    "-=": TokenType.SUB_ASSIGN,
    "*=": TokenType.MUL_ASSIGN,
    "/=": TokenType.DIV_ASSIGN,
    "==": TokenType.EQUAL,
    "!=": TokenType.NOT_EQUAL,
    ">":  TokenType.GT,
    "<":  TokenType.LT,
    ">=": TokenType.GT_EQUAL,
    "<=": TokenType.LT_EQUAL,
}

PUNCTUATION = {
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ",": TokenType.COMMA,
    ":": TokenType.COLON,
    ";": TokenType.SEMI_COLON,
    ".": TokenType.DOT,
}