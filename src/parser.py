"""Turn tokens into an abstract syntax tree for SlayLang.

The parser takes the token stream from the lexer and groups it into statements,
expressions, and blocks that the evaluator can later run.
"""

from nodes import *
from tokens import *

class Parser:
    def __init__(self, tokens):
        """Store the token list and prepare to read it from the first token."""
        self.tokens = tokens

        if self.tokens == []:
            raise Exception(
                "bestie... i got zero tokens. either your lexer is broken "
                "or you fed me an empty file 💀"
            )

        self.index = 0
        self.current_token = self.tokens[self.index]

    def advance(self):
        """Move one step forward through the token list."""
        self.index += 1
        if self.index >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def peek(self):
        """Look ahead at the next token without consuming it."""
        if self.index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.index + 1]

    def parse(self):
        """Read every top-level statement and wrap them in one program node."""
        statements = []

        while True:
            if self.current_token is None:
                raise Exception(
                    f"Line {self.current_token.line}: ran clean off the end of the token list without ever "
                    "hitting EOF — that's a lexer bug, not a you-wrote-bad-code problem"
                )
            if self.current_token.type == TokenType.EOF:
                break
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
            else:
                statement = self.parse_statement()
                statements.append(statement)

        return Program(statements)

    def parse_statement(self):
        """Decide what kind of statement comes next and parse it."""
        if self.current_token.type in (TokenType.LET, TokenType.CONST):
            return self.parse_var_declaration()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.parse_function_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.BREAK:
            return self.parse_break_statement()
        elif self.current_token.type == TokenType.CONTINUE:
            return self.parse_continue_statement()
        elif self.current_token.type in INBUILT_FUNCTIONS:
            return self.parse_expression()
        elif self.current_token.type == TokenType.IDENT:
            if self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif self.peek().type == TokenType.LBRACKET:
                return self.parse_index_assignment()
            else:
                return self.parse_expression()
        else:
            raise Exception(
                f"Line {self.current_token.line}: '{self.current_token.value}' (token #{self.index}, "
                f"type {self.current_token.type.name}) can't start a statement. "
                f"a statement starts with vibe/lockedin, sus, grind, cook, yeet, "
                f"a builtin, or an identifier — this is none of those"
            )

    def parse_primary(self):
        """Parse the smallest building blocks of an expression."""
        # if self.current_token.type == TokenType.MINUS:
        #     self.advance()
        #     operand = self.parse_primary()
        #     return BinaryExpression(NumberLiteral(0), "-", operand)
        if self.current_token.type == TokenType.NUMBER:
            node = NumberLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == TokenType.STRING:
            node = StringLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type in BOOLEANS:
            node = BoolLiteral(self.current_token.type == TokenType.TRUE)
            self.advance()
            return node
        elif self.current_token.type == TokenType.NULL:
            self.advance()
            return NullLiteral()
        elif self.current_token.type == TokenType.IDENT:
            name = self.current_token.value
            self.advance()

            if self.current_token is not None and self.current_token.type == TokenType.LPAREN:
                args = self.parse_call_args()
                return CallExpression(name, args)
            elif self.current_token is not None and self.current_token.type == TokenType.LBRACKET:
                self.advance()  # consume '['
                index = self.parse_expression()
                self.advance()  # consume ']'
                node = IndexExpression(name, index)
                while self.current_token is not None and self.current_token.type == TokenType.LBRACKET:
                    self.advance()
                    index = self.parse_expression()
                    self.advance()
                    node = IndexExpression(node, index)
                return node
            else:
                return Identifier(name)
        elif self.current_token.type in INBUILT_FUNCTIONS:
            name = self.current_token.value
            self.advance()

            if self.current_token is not None and self.current_token.type == TokenType.LPAREN:
                args = self.parse_call_args()
                return CallExpression(name, args)
            else:
                # NOTE: this branch used to fall through and return None
                # silently. that's worse than a crash — it lets a typo turn
                # into a mystery bug three function calls downstream.
                raise Exception(
                    f"Line {self.current_token.line}: '{name}' is a builtin, it needs to be called with parens. "
                    f"you wrote it bare like a variable — did you mean '{name}(...)'?"
                )
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            node = self.parse_expression()
            self.advance()
            return node
        elif self.current_token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            while self.current_token.type != TokenType.RBRACKET: 
                if self.current_token.type == TokenType.COMMA:
                    self.advance()
                if self.current_token.type == TokenType.NEWLINE:
                    self.advance()
                    continue
                elements.append(self.parse_expression())
            self.advance()
            return ArrayLiteral(elements)
        else:
            raise Exception(
                f"Line {self.current_token.line}: i don't know how to parse '{self.current_token.value}' "
                f"(token #{self.index}, type {self.current_token.type.name}) — "
                f"that's not a number, string, bool, identifier, builtin, or '('"
            )

    def parse_var_declaration(self):
        """Read a variable or constant declaration and its starting value."""
        constant = self.current_token.type == TokenType.CONST
        self.advance()
        name = self.current_token.value
        self.advance()
        if self.current_token.type == TokenType.LBRACKET:
            self.advance() # skip '['
            self.advance() # skip ']'
        self.advance() # skip '='
        value = self.parse_expression()
        return VarDeclaration(name, value, constant)

    def parse_assignment(self):
        """Read a normal assignment that changes an existing name."""
        name = self.current_token.value
        self.advance()  # skip identifier
        self.advance()  # skip '='
        value = self.parse_expression()
        return VarDeclaration(name, value, False)

    def parse_index_assignment(self):
        """Read an assignment that writes into one or more array positions."""
        name = self.current_token.value
        self.advance()
        
        indexes = []
        while self.current_token.type == TokenType.LBRACKET:
            self.advance()
            indexes.append(self.parse_expression())
            self.advance()
        
        self.advance()
        value = self.parse_expression()
        return IndexAssignment(name, indexes, value)

    def parse_call_args(self):
        """Read the values inside a function call's parentheses."""
        open_index = self.index
        self.advance()  # consume '('
        args = []
        while self.current_token is not None and self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.COMMA:
                self.advance()
            args.append(self.parse_expression())

        if self.current_token is None:
            raise Exception(
                f"Line {self.current_token.line}: opened '(' at token #{open_index} and never found the matching "
                f"')' — i ran straight off the end of the file looking for it"
            )

        self.advance()  # consume ')'
        return args

    def parse_expression(self):
        """Parse a complete expression, starting with comparison level rules."""
        return self.parse_comparison()

    def parse_comparison(self):
        """Parse comparison expressions like equal to, less than, and greater than."""
        left = self.parse_additive()
        while self.current_token is not None and self.current_token.type in (
            TokenType.EQUAL, TokenType.NOT_EQUAL,
            TokenType.GT, TokenType.LT, TokenType.GT_EQUAL, TokenType.LT_EQUAL
        ):
            operator = self.current_token.value
            self.advance()
            right = self.parse_additive()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_additive(self):
        """Parse expressions that use plus or minus."""
        left = self.parse_term()
        while self.current_token is not None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_term(self):
        """Parse expressions that use multiply, divide, modulo, or floor divide."""
        left = self.parse_power()
        while self.current_token is not None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO, TokenType.FLOOR_DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_power(self):
        """Parse power expressions that use the double-star operator."""
        left = self.parse_unary()
        if self.current_token is not None and self.current_token.type == TokenType.POWER:
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()  # right-associative: 2**3**2 = 2**9
            return BinaryExpression(left, operator, right)
        return left

    def parse_unary(self):
        """Parse one-value operators like a leading minus sign."""
        if self.current_token is not None and self.current_token.type == TokenType.MINUS:
            self.advance()
            operand = self.parse_unary()
            return BinaryExpression(NumberLiteral(0), "-", operand)
        return self.parse_primary()

    def parse_block(self):
        """Read every statement inside one pair of braces."""
        statements = []
        while self.current_token is not None and self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
            else:
                statements.append(self.parse_statement())

        if self.current_token is None:
            raise Exception(
                "Line {self.current_token.line}: you opened a block with '{' and never closed it — i hit the "
                "end of the file still waiting for a '}'"
            )

        self.advance()  # consume '}'
        return statements

    def parse_if_statement(self):
        """Parse a full if statement, including any else-if or else part."""
        self.advance()  # skip 'sus'
        self.advance()  # skip '('
        condition = self.parse_expression()
        self.advance()  # skip ')'
        self.advance()  # skip '{'

        body = self.parse_block()
        else_body = None

        if self.current_token.type == TokenType.ELSE_IF:
            else_body = self.parse_if_statement()
        elif self.current_token.type == TokenType.ELSE:
            self.advance()  # skip 'tho'
            self.advance()  # skip '{'
            else_body = self.parse_block()

        return IfStatement(condition, body, else_body)

    def parse_while_statement(self):
        """Parse a while loop with its condition and body."""
        self.advance()  # skip 'grind'
        self.advance()  # skip '('
        condition = self.parse_expression()
        self.advance()  # skip ')'
        self.advance()  # skip '{'

        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_for_statement(self):
        """Parse a for loop with its start, test, update, and body sections."""
        self.advance()  # skip 'spin'
        self.advance()  # skip '('

        init = self.parse_var_declaration()
        if self.current_token.type == TokenType.SEMI_COLON:
            self.advance()                         # skip ';'
        else:
            raise Exception(f"Line {self.current_token.line}: You missed a colon")
        condition = self.parse_expression()    # e.g. i < 10
        if self.current_token.type == TokenType.SEMI_COLON:
            self.advance()                         # skip ';'
        else:
            raise Exception(f"Line {self.current_token.line}: You missed a colon")
        update = self.parse_assignment()       # e.g. i = i + 1

        self.advance()  # skip ')'
        self.advance()  # skip '{'
        body = self.parse_block()

        return ForStatement(init, condition, update, body)

    def parse_return_statement(self):
        """Parse a return statement and the value it sends back."""
        self.advance()  # skip 'yeet'
        return ReturnStatement(self.parse_expression())

    def parse_break_statement(self):
        """Parse a break statement that stops the current loop."""
        self.advance()  # skip 'dip'
        return BreakStatement()
    
    def parse_continue_statement(self):
        """Parse a continue statement that jumps to the next loop round."""
        self.advance() # skip 'skip'
        return ContinueStatement()

    def parse_function_declaration(self):
        """Parse a function name, its parameter list, and its body."""
        self.advance()  # skip 'cook'
        name = self.current_token.value
        self.advance()  # skip function name
        self.advance()  # skip '('

        params = []
        while self.current_token.type != TokenType.RPAREN:
            if self.current_token.type == TokenType.COMMA:
                self.advance()
            params.append(self.current_token.value)
            self.advance()

        self.advance()  # skip ')'
        self.advance()  # skip '{'
        body = self.parse_block()

        return FunctionDeclaration(name, params, body)


if __name__ == "__main__":
    """Show a tiny parser demo when the file is run by itself."""
    from lexer import Lexer

    lexer = Lexer('cook greet(name, age) {\nyap(name)\n}')
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)