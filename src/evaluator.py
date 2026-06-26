# evaluator.py

from nodes import *
from tokens import *


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class Evaluator:
    def __init__(self):
        self.env = {}
        self.builtins = {
            "yap":    lambda args: print(*args),
            "rant":   lambda args: print(*args, "!!"),
            "snoop": lambda args: input(args[0] if args else ""),
            "floatify": lambda args: float(args[0]),
            "intify": lambda args: int(args[0])
        }        

    def evaluate(self, node):
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
                try:
                    for statement in node.body:
                        self.evaluate(statement)
                except BreakException:
                    break
                except ContinueException:
                    continue

        elif isinstance(node, ForStatement):
            self.evaluate(node.init)
            while self.evaluate(node.condition):
                try:
                    for statement in node.body:
                        self.evaluate(statement)
                except BreakException:
                    break
                except ContinueException:
                    self.evaluate(node.update)
                    continue
                self.evaluate(node.update)

        elif isinstance(node, ReturnStatement):
            # Use an exception to unwind the call stack rather than threading
            # a return value back through every recursive evaluate() call.
            raise ReturnException(self.evaluate(node.value))
        
        elif isinstance(node, BreakStatement):
            raise BreakException()

        elif isinstance(node, ContinueStatement):
            raise ContinueException()

        elif isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            numeric = (int, float)
            if type(left) != type(right) and node.operator not in ("==", "!=") and not (isinstance(left, numeric) and isinstance(right, numeric)):
                raise Exception(f"bestie NO. you can't do {type(left).__name__} {node.operator} {type(right).__name__}, that's not it 💀")
            elif node.operator == "+":
                return left + right
            elif node.operator == "-":
                return left - right
            elif node.operator == "*":
                return left * right
            elif node.operator == "/":
                if right == 0:
                    raise Exception("bestie... you can divide by zero....")
                return left / right
            elif node.operator == "\\":
                if right == 0:
                    raise Exception("bestie... you can divide by zero....")
                return left // right
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

            previous_env = self.env
            local_env = dict(previous_env)  # inherit globals so other functions are visible
            local_env.update({
                param: {"value": arg, "constant": False}
                for param, arg in zip(function.params, args)
            })

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