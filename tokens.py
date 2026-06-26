from enum import Enum


class TokenType(Enum):

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
    MODULO      = "MODULO"
    POWER       = "POWER"

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
    NUMIFY      = "NUMIFY"
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

INBUILT_FUNCTIONS = {TokenType.PRINT, TokenType.PRINT_LOUD, TokenType.INPUT, TokenType.NUMIFY}

BOOLEANS = {TokenType.TRUE, TokenType.FALSE}

BINARY_OPERATORS = {
    TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
    TokenType.DIVIDE, TokenType.MODULO, TokenType.POWER,
    TokenType.EQUAL, TokenType.NOT_EQUAL,
    TokenType.GT, TokenType.LT, TokenType.GT_EQUAL, TokenType.LT_EQUAL,
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
    "numify": TokenType.NUMIFY,
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