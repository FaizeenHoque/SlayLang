from nodes import *
from tokens import *


class ReturnException(Exception):
    """
    Control-flow exception used to unwind the call stack on a return statement.

    Raised by the evaluator when a ReturnStatement node is encountered inside
    a function body. Caught by the CallExpression handler, which extracts the
    return value and resumes normal execution in the caller's environment.

    Attributes:
        value (any): The evaluated return value to be handed back to the caller.
    """

    def __init__(self, value):
        """
        Initialize the ReturnException with the value being returned.

        Args:
            value (any): The evaluated result of the return expression.
        """
        self.value = value


class Evaluator:
    """
    Tree-walking interpreter that evaluates an AST produced by the Parser.

    The Evaluator performs a single-pass recursive walk over the AST,
    executing each node in place. State is maintained in a flat environment
    dictionary (self.env) that maps variable and function names to their
    stored values. Function calls temporarily swap out the global environment
    for a local one, restoring it on return.

    Attributes:
        env (dict): The current variable/function environment. Each variable
            entry is a dict of the form {"value": <any>, "constant": <bool>}.
            Function entries store the raw FunctionDeclaration node directly.
    """

    def __init__(self):
        """
        Initialize the Evaluator with an empty environment.
        """
        self.env = {}
        self.builtins = {
            "yap":    lambda args: print(*args),
            "rant":   lambda args: print(*args, "!!"),
            "snoop": lambda args: input(args[0] if args else ""),
            "numify": lambda args: float(args[0]),
        }        

    def evaluate(self, node):
        """
        Recursively evaluate an AST node and return its result.

        Dispatches on the concrete type of *node*, executing the appropriate
        semantics for each node kind. Statement nodes (Program, VarDeclaration,
        IfStatement, WhileStatement, FunctionDeclaration, ReturnStatement)
        produce side-effects and return None. Expression nodes (BinaryExpression,
        CallExpression, NumberLiteral, StringLiteral, BoolLiteral, Identifier)
        return a Python value.

        Args:
            node (ASTNode): Any node produced by the Parser.

        Returns:
            any: The result of evaluating an expression node, or None for
            statement nodes that do not produce a value.

        Raises:
            Exception: If a constant variable is reassigned.
            Exception: If a binary operator is applied to incompatible types
                (except == and !=, which allow cross-type comparison).
            Exception: If an undefined variable or function name is referenced.
            Exception: If an unknown node type is passed (falls through all
                branches silently — currently no catch-all guard).
            ReturnException: Raised internally when a ReturnStatement is
                evaluated; expected to be caught by the CallExpression handler.
        """
        if isinstance(node, Program):
            for statement in node.statements:
                self.evaluate(statement)

        elif isinstance(node, VarDeclaration):
            if node.name in self.env and self.env[node.name]["constant"]:
                raise Exception(f"nah fam, {node.name} is a const. you can't touch it.")
            self.env[node.name] = {"value": self.evaluate(node.value), "constant": node.constant}

        elif isinstance(node, FunctionDeclaration):
            # Store the raw node so the CallExpression handler can access
            # params and body at call time.
            self.env[node.name] = node

        elif isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                for statement in node.body:
                    self.evaluate(statement)
            elif node.else_body is not None:
                if isinstance(node.else_body, IfStatement):
                    # else-if chain: delegate back to evaluate so the full
                    # condition/body/else_body logic is reused.
                    self.evaluate(node.else_body)
                else:
                    for statement in node.else_body:
                        self.evaluate(statement)

        elif isinstance(node, WhileStatement):
            while (self.evaluate(node.condition)):
                for statement in node.body:
                    self.evaluate(statement)

        elif isinstance(node, ReturnStatement):
            # Use an exception to unwind the call stack rather than threading
            # a return value back through every recursive evaluate() call.
            raise ReturnException(self.evaluate(node.value))

        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if type(left) != type(right) and node.operator not in ("==", "!="):
                raise Exception(f"bestie NO. you can't do {type(left).__name__} {node.operator} {type(right).__name__}, that's not it 💀")
            elif node.operator == "+":
                return left + right
            elif node.operator == "-":
                return left - right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                return left / right
            elif node.operator == "%":
                return left % right
            elif node.operator == "**":
                return left ** right
            elif node.operator == "==":
                return left == right
            elif node.operator == "!=":
                return left != right
            elif node.operator == ">":
                return left > right
            elif node.operator == "<":
                return left < right
            elif node.operator == ">=":
                return left >= right
            elif node.operator == "<=":
                return left <= right

        elif isinstance(node, CallExpression):
            if node.name in self.builtins:
                args = [self.evaluate(arg) for arg in node.args]
                return self.builtins[node.name](args)

            # --- User-defined function call ---
            # Evaluate all arguments in the *caller's* environment before
            # swapping to the local scope.
            args = [self.evaluate(arg) for arg in node.args]

            if node.name in self.env:
                function = self.env[node.name]
            else:
                raise Exception(f"where did u find '{node.name}', ion see it in the env")

            # Build a fresh local environment from params and evaluated args.
            # Functions cannot currently close over the outer environment
            # (no closure support).
            local_env = {
                param: {"value": arg, "constant": False}
                for param, arg in zip(function.params, args)
            }

            previous_env = self.env
            self.env = local_env
            try:
                for statement in function.body:
                    self.evaluate(statement)
            except ReturnException as e:
                self.env = previous_env
                return e.value
            self.env = previous_env

        elif isinstance(node, NumberLiteral):
            return node.value

        elif isinstance(node, StringLiteral):
            return node.value

        elif isinstance(node, BoolLiteral):
            return node.value

        elif isinstance(node, Identifier):
            if node.name in self.env:
                return self.env[node.name]["value"]
            else:
                raise Exception(f"buddy, variable {node.name} does NOT exist")