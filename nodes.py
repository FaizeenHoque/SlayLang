class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program(statements={self.statements})"


# Declarations

class VarDeclaration:
    def __init__(self, name, value, constant):
        self.name = name
        self.value = value
        self.constant = constant

    def __repr__(self):
        return f"VarDeclaration(name={self.name}, value={self.value}, constant={self.constant})"


class FunctionDeclaration:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration(name={self.name}, params={self.params}, body={self.body})"


# Statements

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

class ForStatement:
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"ForStatement(init={self.init}, condition={self.condition}, update={self.update}, body={self.body})"

class ReturnStatement:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnStatement(value={self.value})"


# Expressions

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


# Literals & identifiers

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