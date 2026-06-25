class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        
        if self.tokens == []:
            raise Exception("bestie... no tokens to parse 💀")

        self.index = 0
        self.current_token = self.tokens[self.index]
    def advance(self):
        self.index+=1
        if self.index >= len(self.tokens):
            self.current_token = None
        else:
            self.current_token = self.tokens[self.index]
    def peek(self):
        if self.index + 1 >= len(self.tokens):
            return None
        return self.tokens[self.index+1]

    def parse(self):
        statements = []

        while self.current_token.type != "EOF":
            # skip new lines
            if self.current_token.type == "NEWLINE":
                self.advance()
            else:
                statement = self.parse_statement()
                statements.append(statement)
        
        return Program(statements)
    
    def parse_statement(self):
        if self.current_token.type in ("LET", "CONST"):
            return self.parse_var_declaration()
        elif self.current_token.type == "IF":
            return self.parse_if_statement()
        elif self.current_token.type == "WHILE":
            return self.parse_while_statement()
        elif self.current_token.type == "FUNCTION":
            return self.parse_function_declaration()
        elif self.current_token.type == "RETURN":
            return self.parse_return_statement()
        elif self.current_token.type in ("PRINT", "PRINT_LOUD", "INPUT"):
            return self.parse_expression()
        elif self.current_token.type == "IDENT":
            return self.parse_expression()
        else:
            raise Exception(f"my guy.. never seen '{self.current_token.type}' in my life btw")

    def parse_var_declaration(self):
        constant = self.current_token.type == "CONST" # is constant? if yes, return true - else, false
        self.advance()
        name = self.current_token.value
        self.advance()
        self.advance() # skip ASSIGN
        value = self.parse_expression() 
        return VarDeclaration(name, value, constant)
    
    def parse_expression(self):
        if self.current_token.type == "NUMBER":
            node = NumberLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == "STRING":
            node = StringLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type in ("TRUE", "FALSE"):
            node = BoolLiteral(self.current_token.value)
            self.advance()
            return node
        elif self.current_token.type == "IDENT":
            name = self.current_token.value
            self.advance()

            if self.current_token.type is not None and self.current_token.type == "LPAREN":
                args = self.parse_call_args()
                return CallExpression(name, args)
            else:
                return Identifier(name)
        elif self.current_token.type in ("PRINT", "PRINT_LOUD", "INPUT"):
            name = self.current_token.value  
            self.advance()
            
            if self.current_token.type is not None and self.current_token.type == "LPAREN":
                args = self.parse_call_args()
                return CallExpression(name, args)
        else:
            raise Exception(f"i dont know how you expect me to parse expression {self.current_token.value}")
    
    def parse_call_args(self):
        self.advance()
        args = []
        while self.current_token.type is not None and self.current_token.type != "RPAREN":
            if self.current_token.type == "COMMA":
                self.advance()
            args.append(self.parse_expression())
        self.advance()
        return args


class VarDeclaration:
    def __init__(self, name, value, constant):
        self.name = name
        self.value = value
        self.constant = constant
    def __repr__(self):
        return f"VarDeclaration(name={self.name}, value={self.value}, constant={self.constant})"

class NumberLiteral:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberLiteral(value={self.value})"

class StringLiteral:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringLiteral(value={self.value})"

class BoolLiteral:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BoolLiteral(value={self.value})"

class Identifier:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier(name={self.name})"

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"BinaryExpression(left={self.left}, operator={self.operator}, right={self.right})"

class CallExpression:
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"CallExpression(name={self.name}, args={self.args})"

class ReturnStatement:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"ReturnStatement(value={self.value})"

class IfStatement:
    def __init__(self, condition, body, else_body):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        return f"IfStatement(condition={self.condition}, body={self.body}, else_body={self.else_body})"

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"FunctionDeclaration(name={self.name}, params={self.params}, body={self.body})"

class Program:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program(statements={self.statements})"

if __name__ == "__main__":
    from lexer import Lexer
    
    lexer = Lexer('yap("whats up pookie bear")')
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)