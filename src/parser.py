# parser.py

from nodes import *
from tokens import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

        if self.tokens == []:
            raise Exception(
                "bestie... i got zero tokens. either your lexer is broken "
                "or you fed me an empty file 💀"
            )

        self.index = 0
        self.current_token = self.tokens[self.index]

    def advance(self):
        self.index += 1
        if self.index >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]

    def peek(self):
        if self.index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.index + 1]

    def parse(self):
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
        if self.current_token.type == TokenType.MINUS:
            self.advance()
            operand = self.parse_primary()
            return BinaryExpression(NumberLiteral(0), "-", operand)
        elif self.current_token.type == TokenType.NUMBER:
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
        name = self.current_token.value
        self.advance()  # skip identifier
        self.advance()  # skip '='
        value = self.parse_expression()
        return VarDeclaration(name, value, False)

    def parse_index_assignment(self):
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
        left = self.parse_primary()

        while self.current_token is not None and self.current_token.type in BINARY_OPERATORS:
            operator = self.current_token.value
            self.advance()
            right = self.parse_primary()
            left = BinaryExpression(left, operator, right)

        return left

    def parse_block(self):
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
        self.advance()  # skip 'grind'
        self.advance()  # skip '('
        condition = self.parse_expression()
        self.advance()  # skip ')'
        self.advance()  # skip '{'

        body = self.parse_block()
        return WhileStatement(condition, body)

    def parse_for_statement(self):
        self.advance()  # skip 'spin'
        self.advance()  # skip '('

        init = self.parse_var_declaration()    # e.g. vibe i = 0
        if self.current_token.type == TokenType.SEMI_COLON:
            self.advance()                         # skip ';'
        else:
            raise Exception("Line {self.current_token.line}: You missed a colon")
        condition = self.parse_expression()    # e.g. i < 10
        if self.current_token.type == TokenType.SEMI_COLON:
            self.advance()                         # skip ';'
        else:
            raise Exception("Line {self.current_token.line}: You missed a colon")
        update = self.parse_assignment()       # e.g. i = i + 1

        self.advance()  # skip ')'
        self.advance()  # skip '{'
        body = self.parse_block()

        return ForStatement(init, condition, update, body)

    def parse_return_statement(self):
        self.advance()  # skip 'yeet'
        return ReturnStatement(self.parse_expression())

    def parse_break_statement(self):
        self.advance()  # skip 'dip'
        return BreakStatement()
    
    def parse_continue_statement(self):
        self.advance() # skip 'skip'
        return ContinueStatement()

    def parse_function_declaration(self):
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
    from lexer import Lexer

    lexer = Lexer('cook greet(name, age) {\nyap(name)\n}')
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)