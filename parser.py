from nodes import *
from tokens import *

class Parser:
    """
    Parses a flat list of tokens into an Abstract Syntax Tree (AST).

    The parser uses recursive descent to handle operator precedence and
    nested expressions. It consumes tokens produced by the Lexer and
    builds a Program node whose children represent every top-level
    statement in the source.

    Attributes:
        tokens (list): The full list of Token objects to parse.
        index (int): The current position in the token list.
        current_token (Token): The token at the current index.
    """

    def __init__(self, tokens):
        """
        Initialize the Parser with a list of tokens.

        Args:
            tokens (list): A non-empty list of Token objects.

        Raises:
            Exception: If the token list is empty.
        """
        self.tokens = tokens
        
        if self.tokens == []:
            raise Exception("bestie... no tokens to parse 💀")

        self.index = 0
        self.current_token = self.tokens[self.index]

    def advance(self):
        """
        Move to the next token in the list.

        Increments the index and updates current_token. If the end of
        the token list is reached, current_token is set to None.
        """
        self.index += 1
        if self.index >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def peek(self):
        """
        Look at the next token without consuming it.

        Returns:
            Token | None: The token immediately after the current one,
            or None if the current token is the last in the list.
        """
        if self.index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.index + 1]

    def parse(self):
        """
        Parse the entire token stream into a Program AST node.

        Iterates over all tokens, skipping newlines and delegating each
        non-trivial token to parse_statement(), until the EOF token is
        reached.

        Returns:
            Program: The root AST node containing all top-level statements.
        """
        statements = []

        while self.current_token.type != TokenType.EOF:
            # skip new lines
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
            else:
                statement = self.parse_statement()
                statements.append(statement)
        
        return Program(statements)
    
    def parse_statement(self):
        """
        Parse a single statement based on the current token type.

        Dispatches to the appropriate sub-parser depending on what kind
        of statement starts at the current token.

        Returns:
            ASTNode: One of VarDeclaration, IfStatement, WhileStatement,
            FunctionDeclaration, ReturnStatement, or an expression node.

        Raises:
            Exception: If the current token does not begin a valid statement.
        """
        if self.current_token.type in (TokenType.LET, TokenType.CONST):
            return self.parse_var_declaration()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.current_token.type in INBUILT_FUNCTIONS:
            return self.parse_expression()
        elif self.current_token.type == TokenType.IDENT:
            return self.parse_expression()
        else:
            raise Exception(f"my guy.. never seen '{self.current_token.value}' in my life btw")

    def parse_primary(self):
        """
        Parse a primary (atomic) expression.

        Handles the smallest indivisible units of an expression:
        number literals, string literals, boolean literals, identifiers
        (which may be followed by a call argument list), built-in
        function calls, and parenthesised sub-expressions.

        Returns:
            ASTNode: One of NumberLiteral, StringLiteral, BoolLiteral,
            Identifier, or CallExpression; or the result of a recursive
            parse_expression() call for parenthesised groups.

        Raises:
            Exception: If the current token cannot start a primary expression.
        """
        if self.current_token.type == TokenType.NUMBER:
            node = NumberLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == TokenType.STRING:
            node = StringLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type in BOOLEANS:
            node = BoolLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == TokenType.IDENT:
            name = self.current_token.value
            self.advance()

            if self.current_token.type is not None and self.current_token.type == TokenType.LPAREN:
                args = self.parse_call_args()
                return CallExpression(name, args)
            else:
                return Identifier(name)
        elif self.current_token.type in INBUILT_FUNCTIONS:
            name = self.current_token.value  
            self.advance()
            
            if self.current_token.type is not None and self.current_token.type == TokenType.LPAREN:
                args = self.parse_call_args()
                return CallExpression(name, args)
        elif self.current_token.type == TokenType.LPAREN:  
            self.advance()
            node = self.parse_expression()
            self.advance()
            return node
        else:
            raise Exception(f"i dont know how you expect me to parse expression {self.current_token.value}")
    
    def parse_var_declaration(self):
        """
        Parse a variable declaration statement (let or const).

        Expects the form:  <let|const> <identifier> = <expression>

        Advances past the keyword, reads the variable name, skips the
        assignment operator, then delegates to parse_expression() for
        the initialiser value.

        Returns:
            VarDeclaration: AST node holding the variable name, its
            initial value expression, and whether it is constant.
        """
        constant = self.current_token.type == TokenType.CONST
        self.advance()
        name = self.current_token.value
        self.advance()
        self.advance()  # skip the '=' token
        value = self.parse_expression() 
        return VarDeclaration(name, value, constant)
    
    def parse_call_args(self):
        """
        Parse the argument list of a function call.

        Expects the current token to be '(' on entry. Reads comma-
        separated primary expressions until the matching ')' is found,
        then advances past it.

        Returns:
            list[ASTNode]: A (possibly empty) list of argument nodes,
            each produced by parse_primary().
        """
        self.advance()  # consume '('
        args = []
        while self.current_token.type is not None and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.COMMA:
                self.advance()
            args.append(self.parse_primary())
        self.advance()  # consume ')'
        return args

    def parse_expression(self):
        """
        Parse a binary expression with left-to-right associativity.

        Starts by parsing a primary expression as the left-hand operand,
        then repeatedly consumes binary operators and right-hand primaries
        to build a left-associative BinaryExpression tree.

        Returns:
            ASTNode: A single primary node if no binary operator follows,
            or a (possibly nested) BinaryExpression node otherwise.
        """
        left = self.parse_primary()

        while self.current_token is not None and self.current_token.type in BINARY_OPERATORS:
            operator = self.current_token.value
            self.advance()
            right = self.parse_primary()
            left = BinaryExpression(left, operator, right)
        
        return left
    
    def parse_block(self):
        """
        Parse a brace-delimited block of statements.

        Expects the opening '{' to have already been consumed. Reads
        statements until the closing '}' is reached, skipping any
        newlines in between, then consumes the '}'.

        Returns:
            list[ASTNode]: The statements found inside the block.
        """
        statements = []
        while self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
            else:
                statements.append(self.parse_statement())
        self.advance()
        return statements

    def parse_if_statement(self):
        """
        Parse an if / else-if / else statement.

        Handles the full conditional chain: an initial 'sus' branch,
        zero or more 'mid' (else-if) branches parsed recursively, and
        an optional 'tho' (else) branch.

        Returns:
            IfStatement: AST node containing the condition, the if-body,
            and optionally a chained IfStatement or else block as
            else_body.
        """
        self.advance() # skip sus
        self.advance() # skip (
        condition = self.parse_expression()
        self.advance() # skip )
        self.advance() # skip {

        body = self.parse_block()
        else_body = None

        if self.current_token.type == TokenType.ELSE_IF:
            else_body = self.parse_if_statement()
        elif self.current_token.type == TokenType.ELSE:
            self.advance() # skip tho
            self.advance() # skip {
            else_body = self.parse_block()
        
        return IfStatement(condition, body, else_body)
    
    def parse_while_statement(self):
        """
        Parse a while loop statement.

        Expects the form:  grind (<condition>) { <body> }

        Consumes the 'grind' keyword, the parenthesised condition, and
        the braced body block.

        Returns:
            WhileStatement: AST node containing the condition expression
            and the list of body statements.
        """
        self.advance() # skip grind
        self.advance() # skip (
        condition = self.parse_expression()
        self.advance() # skip )
        self.advance() # skip {

        body = self.parse_block()
        return WhileStatement(condition, body)
    
    def parse_return_statement(self):
        """
        Parse a return statement.

        Consumes the 'yeet' keyword then parses the expression whose
        value will be returned.

        Returns:
            ReturnStatement: AST node wrapping the return value expression.
        """
        self.advance() # skip yeet
        return ReturnStatement(self.parse_expression())
    
    def parse_function_declaration(self):
        """
        Parse a function declaration.

        Expects the form:  cook <name>(<params>) { <body> }

        Consumes the 'cook' keyword, the function name, the
        comma-separated parameter list, and the braced body block.

        Returns:
            FunctionDeclaration: AST node containing the function name,
            its parameter list, and its body statements.
        """
        self.advance() # skip cook
        name = self.current_token.value
        self.advance() # skip name
        self.advance() # skip (
        
        params = []
        while self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.COMMA:
                self.advance()
            params.append(self.current_token.value)
            self.advance()
        
        self.advance() # skip )
        self.advance() # skip {
        body = self.parse_block()

        return FunctionDeclaration(name, params, body)

if __name__ == "__main__":
    from lexer import Lexer
    
    lexer = Lexer('cook greet(name, age) {\nyap(name)\n}')
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)