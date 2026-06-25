class Program:
    """
    Root node of the AST, representing an entire source file.

    Attributes:
        statements (list[ASTNode]): All top-level statements in the program,
            in the order they appear in the source.
    """

    def __init__(self, statements):
        """
        Args:
            statements (list[ASTNode]): The top-level statements parsed from
                the source.
        """
        self.statements = statements

    def __repr__(self):
        return f"Program(statements={self.statements})"


# Declarations

class VarDeclaration:
    """
    AST node for a variable declaration (let or const).

    Attributes:
        name (str): The variable name.
        value (ASTNode): The expression assigned to the variable.
        constant (bool): True if declared with const, False for let.
    """

    def __init__(self, name, value, constant):
        """
        Args:
            name (str): The variable name.
            value (ASTNode): The initialiser expression.
            constant (bool): Whether the variable is immutable.
        """
        self.name = name
        self.value = value
        self.constant = constant

    def __repr__(self):
        return f"VarDeclaration(name={self.name}, value={self.value}, constant={self.constant})"


class FunctionDeclaration:
    """
    AST node for a named function definition.

    Attributes:
        name (str): The function name.
        params (list[str]): The parameter names, in order.
        body (list[ASTNode]): The statements that make up the function body.
    """

    def __init__(self, name, params, body):
        """
        Args:
            name (str): The function name.
            params (list[str]): Ordered list of parameter names.
            body (list[ASTNode]): Statements inside the function body.
        """
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDeclaration(name={self.name}, params={self.params}, body={self.body})"


# Statements

class IfStatement:
    """
    AST node for an if / else-if / else statement.

    Attributes:
        condition (ASTNode): The expression evaluated to decide the branch.
        body (list[ASTNode]): Statements executed when condition is truthy.
        else_body (list[ASTNode] | None): Statements executed in the else
            branch, or None if there is no else clause.
    """

    def __init__(self, condition, body, else_body):
        """
        Args:
            condition (ASTNode): The branch condition expression.
            body (list[ASTNode]): The if-branch statements.
            else_body (list[ASTNode] | None): The else-branch statements,
                or None.
        """
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, body={self.body}, else_body={self.else_body})"


class WhileStatement:
    """
    AST node for a while loop.

    Attributes:
        condition (ASTNode): The expression evaluated before each iteration.
        body (list[ASTNode]): Statements executed on each iteration.
    """

    def __init__(self, condition, body):
        """
        Args:
            condition (ASTNode): The loop condition expression.
            body (list[ASTNode]): The loop body statements.
        """
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"


class ReturnStatement:
    """
    AST node for a return statement inside a function.

    Attributes:
        value (ASTNode | None): The expression to return, or None for a
            bare return.
    """

    def __init__(self, value):
        """
        Args:
            value (ASTNode | None): The return value expression, or None.
        """
        self.value = value

    def __repr__(self):
        return f"ReturnStatement(value={self.value})"


# Expressions

class BinaryExpression:
    """
    AST node for a binary infix expression (e.g. a + b, x == y).

    Attributes:
        left (ASTNode): The left-hand operand.
        operator (str): The operator symbol (e.g. '+', '==', '**').
        right (ASTNode): The right-hand operand.
    """

    def __init__(self, left, operator, right):
        """
        Args:
            left (ASTNode): The left-hand operand expression.
            operator (str): The operator as a string.
            right (ASTNode): The right-hand operand expression.
        """
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression(left={self.left}, operator={self.operator}, right={self.right})"


class CallExpression:
    """
    AST node for a function call (built-in or user-defined).

    Attributes:
        name (str): The name of the function being called.
        args (list[ASTNode]): The argument expressions, in order.
    """

    def __init__(self, name, args):
        """
        Args:
            name (str): The function name.
            args (list[ASTNode]): The argument expressions passed to the call.
        """
        self.name = name
        self.args = args

    def __repr__(self):
        return f"CallExpression(name={self.name}, args={self.args})"


# Literals & identifiers

class NumberLiteral:
    """
    AST node for a numeric literal (int or float).

    Attributes:
        value (int | float): The numeric value.
    """

    def __init__(self, value):
        """
        Args:
            value (int | float): The numeric value from the source.
        """
        self.value = value

    def __repr__(self):
        return f"NumberLiteral(value={self.value})"


class StringLiteral:
    """
    AST node for a string literal.

    Attributes:
        value (str): The string contents, excluding surrounding quotes.
    """

    def __init__(self, value):
        """
        Args:
            value (str): The string contents.
        """
        self.value = value

    def __repr__(self):
        return f"StringLiteral(value={self.value})"


class BoolLiteral:
    """
    AST node for a boolean literal (facts / cap).

    Attributes:
        value (str): The raw keyword value ('facts' or 'cap').
    """

    def __init__(self, value):
        """
        Args:
            value (str): The raw boolean keyword from the source.
        """
        self.value = value

    def __repr__(self):
        return f"BoolLiteral(value={self.value})"


class Identifier:
    """
    AST node for a variable or parameter reference.

    Attributes:
        name (str): The identifier name as it appears in the source.
    """

    def __init__(self, name):
        """
        Args:
            name (str): The identifier name.
        """
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name})"