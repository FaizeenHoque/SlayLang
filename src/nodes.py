"""Define the small tree-shaped objects used to store parsed SlayLang code.

The parser builds these node objects after reading source text. The evaluator
then walks these nodes to run the program step by step.
"""

class Program:
    def __init__(self, statements):
        """Store the full list of top-level statements in one program."""
        self.statements = statements

    def __repr__(self):
        """Show the program node in a readable debug form."""
        return f"Program(statements={self.statements})"


# Declarations

class VarDeclaration:
    def __init__(self, name, value, constant):
        """Store a variable name, the value it should hold, and whether it is constant."""
        self.name = name
        self.value = value
        self.constant = constant

    def __repr__(self):
        """Show the variable declaration in a readable debug form."""
        return f"VarDeclaration(name={self.name}, value={self.value}, constant={self.constant})"


class FunctionDeclaration:
    def __init__(self, name, params, body):
        """Store a function name, its parameter names, and its body statements."""
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        """Show the function declaration in a readable debug form."""
        return f"FunctionDeclaration(name={self.name}, params={self.params}, body={self.body})"


# Statements

class IfStatement:
    def __init__(self, condition, body, else_body):
        """Store the condition, main body, and optional else branch for an if statement."""
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        """Show the if statement in a readable debug form."""
        return f"IfStatement(condition={self.condition}, body={self.body}, else_body={self.else_body})"


class WhileStatement:
    def __init__(self, condition, body):
        """Store the condition and body for a while loop."""
        self.condition = condition
        self.body = body

    def __repr__(self):
        """Show the while loop in a readable debug form."""
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class ForStatement:
    def __init__(self, init, condition, update, body):
        """Store the three loop parts and the loop body for a for statement."""
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        """Show the for loop in a readable debug form."""
        return f"ForStatement(init={self.init}, condition={self.condition}, update={self.update}, body={self.body})"

class ReturnStatement:
    def __init__(self, value):
        """Store the value that should be sent back from a function."""
        self.value = value

    def __repr__(self):
        """Show the return statement in a readable debug form."""
        return f"ReturnStatement(value={self.value})"

class BreakStatement:
    """Mark a break statement so loops know when to stop early."""
    pass

class ContinueStatement:
    """Mark a continue statement so loops know to skip to the next round."""
    pass


# Expressions

class BinaryExpression:
    def __init__(self, left, operator, right):
        """Store the left side, operator, and right side of a two-part expression."""
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        """Show the binary expression in a readable debug form."""
        return f"BinaryExpression(left={self.left}, operator={self.operator}, right={self.right})"


class CallExpression:
    def __init__(self, name, args):
        """Store the name being called and the list of values passed to it."""
        self.name = name
        self.args = args

    def __repr__(self):
        """Show the call expression in a readable debug form."""
        return f"CallExpression(name={self.name}, args={self.args})"


# Literals & identifiers

class NumberLiteral:
    def __init__(self, value):
        """Store a plain number value."""
        self.value = value

    def __repr__(self):
        """Show the number literal in a readable debug form."""
        return f"NumberLiteral(value={self.value})"


class StringLiteral:
    def __init__(self, value):
        """Store a plain text value."""
        self.value = value

    def __repr__(self):
        """Show the string literal in a readable debug form."""
        return f"StringLiteral(value={self.value})"


class BoolLiteral:
    def __init__(self, value):
        """Store a true or false value."""
        self.value = value

    def __repr__(self):
        """Show the boolean literal in a readable debug form."""
        return f"BoolLiteral(value={self.value})"

class NullLiteral:
    """Mark a null value in the syntax tree."""
    pass


class Identifier:
    def __init__(self, name):
        """Store the name of a variable or other saved value."""
        self.name = name

    def __repr__(self):
        """Show the identifier in a readable debug form."""
        return f"Identifier(name={self.name})"


class ArrayLiteral:
    def __init__(self, elements):
        """Store the values that belong inside one array."""
        self.elements = elements

    def __repr__(self):
        """Show the array literal in a readable debug form."""
        return f"ArrayLiteral(elements={self.elements})"


class IndexExpression:
    def __init__(self, name, index):
        """Store the thing being looked up and the position being used."""
        self.name = name
        self.index = index
        
    def __repr__(self):
        """Show the index lookup in a readable debug form."""
        return f"IndexExpression(name={self.name}, index={self.index})"

class IndexAssignment:
    def __init__(self, name, indexes, value):
        """Store the target name, each index used, and the value to write."""
        self.name = name
        self.indexes = indexes
        self.value = value

    def __repr__(self):
        """Show the indexed assignment in a readable debug form."""
        return f"IndexAssignment(name={self.name}, indexes={self.indexes}, value={self.value})"