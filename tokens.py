from enum import Enum


class TokenType(Enum):
    """
    Enumeration of every token type recognised by the Lexer.

    Members are grouped by category below. The string value of each
    member matches its name and is used for readable repr output.

    Categories
    ----------
    Control flow:
        IF, ELSE_IF, ELSE, WHILE, FOR, FOR_OF, BREAK, CONTINUE,
        RETURN, FUNCTION

    Variables / declarations:
        LET, CONST, ASSIGN, ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN

    Literals:
        NUMBER, STRING, TRUE, FALSE, NULL

    Identifiers & structure:
        IDENT, EOF, NEWLINE

    Arithmetic operators:
        PLUS, MINUS, MULTIPLY, DIVIDE, MODULO, POWER

    Comparison operators:
        EQUAL, NOT_EQUAL, GT, LT, GT_EQUAL, LT_EQUAL

    Logical operators:
        AND, OR, NOT

    Built-in functions:
        PRINT, PRINT_LOUD, INPUT

    Punctuation / delimiters:
        LPAREN, RPAREN, LBRACKET, RBRACKET, LBRACE, RBRACE,
        COMMA, COLON, DOT

    Miscellaneous:
        ARROW, DELETE, IMPORT, TRY, CATCH, THROW
    """

    # Control flow
    IF          = "IF"
    ELSE_IF     = "ELSE_IF"
    ELSE        = "ELSE"
    WHILE       = "WHILE"
    FOR         = "FOR"
    FOR_OF      = "FOR_OF"
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
    DOT         = "DOT"        

    # Miscellaneous
    ARROW       = "ARROW"
    DELETE      = "DELETE"
    IMPORT      = "IMPORT"
    TRY         = "TRY"
    CATCH       = "CATCH"
    THROW       = "THROW"


# Sets used by the parser for quick membership tests

INBUILT_FUNCTIONS = {TokenType.PRINT, TokenType.PRINT_LOUD, TokenType.INPUT}
"""set[TokenType]: Token types that represent built-in callable functions."""

BOOLEANS = {TokenType.TRUE, TokenType.FALSE}
"""set[TokenType]: Token types that represent boolean literals."""

BINARY_OPERATORS = {
    # Arithmetic
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.MULTIPLY,
    TokenType.DIVIDE,
    TokenType.MODULO,
    TokenType.POWER,
    # Comparison
    TokenType.EQUAL,
    TokenType.NOT_EQUAL,
    TokenType.GT,
    TokenType.LT,
    TokenType.GT_EQUAL,
    TokenType.LT_EQUAL,
}
"""set[TokenType]: Token types that can appear as binary infix operators."""


# Lookup tables used by the Lexer to classify character sequences

KEYWORDS = {
    # Booleans / null
    "facts":    TokenType.TRUE,
    "cap":      TokenType.FALSE,
    "ghosted":  TokenType.NULL,

    # Variable declarations
    "vibe":     TokenType.LET,
    "lock":     TokenType.CONST,

    # Conditionals
    "sus":      TokenType.IF,
    "mid":      TokenType.ELSE_IF,
    "tho":      TokenType.ELSE,

    # Loops
    "grind":    TokenType.WHILE,
    "spin":     TokenType.FOR,
    "roam":     TokenType.FOR_OF,

    # Loop control
    "dip":      TokenType.BREAK,
    "skip":     TokenType.CONTINUE,

    # Functions
    "cook":     TokenType.FUNCTION,
    "yeet":     TokenType.RETURN,

    # Modules
    "fw":       TokenType.IMPORT,

    # Error handling
    "no_shot":  TokenType.TRY,
    "ratio":    TokenType.CATCH,
    "flop":     TokenType.THROW,

    # Deletion
    "ghost":    TokenType.DELETE,
}
"""dict[str, TokenType]: Maps reserved keyword strings to their token types."""

BUILTINS = {
    "yap":          TokenType.PRINT,
    "spill":        TokenType.PRINT_LOUD,
    "interrogate":  TokenType.INPUT,
}
"""dict[str, TokenType]: Maps built-in function names to their token types."""

OPERATORS = {
    # Arrow
    "=>":   TokenType.ARROW,

    # Logical
    "&&":   TokenType.AND,
    "||":   TokenType.OR,
    "nah":  TokenType.NOT,

    # Arithmetic
    "+":    TokenType.PLUS,
    "-":    TokenType.MINUS,
    "*":    TokenType.MULTIPLY,
    "/":    TokenType.DIVIDE,
    "%":    TokenType.MODULO,
    "**":   TokenType.POWER,

    # Assignment
    "=":    TokenType.ASSIGN,
    "+=":   TokenType.ADD_ASSIGN,
    "-=":   TokenType.SUB_ASSIGN,
    "*=":   TokenType.MUL_ASSIGN,  
    "/=":   TokenType.DIV_ASSIGN,

    # Comparison
    "==":   TokenType.EQUAL,
    "!=":   TokenType.NOT_EQUAL,
    ">":    TokenType.GT,
    "<":    TokenType.LT,
    ">=":   TokenType.GT_EQUAL,
    "<=":   TokenType.LT_EQUAL,
}
"""dict[str, TokenType]: Maps operator strings to their token types."""

PUNCTUATION = {
    # Parentheses
    "(":    TokenType.LPAREN,
    ")":    TokenType.RPAREN,

    # Brackets
    "[":    TokenType.LBRACKET,
    "]":    TokenType.RBRACKET,

    # Braces
    "{":    TokenType.LBRACE,
    "}":    TokenType.RBRACE,

    # Other
    ",":    TokenType.COMMA,
    ":":    TokenType.COLON,
    ".":    TokenType.DOT,
}
"""dict[str, TokenType]: Maps single punctuation characters to their token types."""