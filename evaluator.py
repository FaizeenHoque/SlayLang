from nodes import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Evaluator:
    def __init__(self):
        self.env = {}
    
    def evaluate(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.evaluate(statement)
        if isinstance(node, VarDeclaration):
            value = self.evaluate(node.value)
            self.env[node.name] = value
        if isinstance(node, FunctionDeclaration):
            self.env[node.name] = node
        if isinstance(node, IfStatement):
            if self.evaluate(node.condition):
                for statement in node.body:
                    self.evaluate(statement)
            elif node.else_body is not None:
                if isinstance(node.else_body, IfStatement):
                    self.evaluate(node.else_body)
                else:
                    for statement in node.else_body:
                            self.evaluate(statement)
        if isinstance(node, WhileStatement):
            while (self.evaluate(node.condition)):
                for statement in node.body:
                    self.evaluate(statement)
        if isinstance(node, ReturnStatement):
            raise ReturnException(self.evaluate(node.value))
        if isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)  
            right = self.evaluate(node.right) 

            if node.operator == "+":
                return left+right
            if node.operator == "-":
                return left-right
            if node.operator == "*":
                return left*right
            if node.operator == "/":
                return left/right
            if node.operator == "%":
                return left%right
            if node.operator == "**":
                return left**right

            if node.operator == "==":
                return left==right
            if node.operator == "!=":
                return left!=right
            if node.operator == ">":
                return left>right
            if node.operator == "<":
                return left<right
            if node.operator == ">=":
                return left>=right
            if node.operator == "<=":
                return left<=right
        if isinstance(node, CallExpression):
            if node.name == "yap":
                evaluated = []
                for arg in node.args:
                    evaluated.append(self.evaluate(arg))
                
                print(*evaluated)
                return
            args = []
            for arg in node.args:
                args.append(self.evaluate(arg))
            function = self.env[node.name]
            local_env = dict(zip(function.params, args))
            previous_env = self.env
            self.env = local_env
            try:
                for statement in function.body:
                    self.evaluate(statement)
            except ReturnException as e:
                self.env = previous_env
                return e.value
            self.env = previous_env        
        if isinstance(node, NumberLiteral):
            return node.value
        if isinstance(node, StringLiteral):
            return node.value
        if isinstance(node, BoolLiteral):
            return node.value
        if isinstance(node, Identifier):
            if node.name in self.env:
                return self.env[node.name]
            else:
                raise Exception(f"buddy, variable {node.name} does NOT exist")