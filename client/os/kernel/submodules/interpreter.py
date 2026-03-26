from .dataclasses import *


class Interpreter:
    def __init__(self):
        self.env = {}
        self.builtins = {
            'outl':                 lambda *args: print(*args),
            'file':                 lambda path: {'system': {'onload': {'modules': ['nucle', 'fsys']}}},
            'modget':               lambda path: None,
        }

    def run(self, statements):
        for node in statements:
            self.exec(node)

    def exec(self, node):
        if isinstance(node, Assign):
            self.env[node.target] = self.eval(node.value)

        elif isinstance(node, While):
            while self.eval(node.condition):
                for stmt in node.body:
                    self.exec(stmt)

        elif isinstance(node, Each):
            for item in self.eval(node.iterable):
                self.env[node.var] = item
                for stmt in node.body:
                    self.exec(stmt)

        elif isinstance(node, Call):
            self.eval(node)

    def eval(self, node):
        if isinstance(node, Literal):
            return node.value

        elif isinstance(node, Name):
            return self.env[node.value]

        elif isinstance(node, Call):
            args = [self.eval(a) for a in node.args]
            if node.func in self.builtins:
                return self.builtins[node.func](*args)

        elif isinstance(node, BinOp):
            l, r = self.eval(node.left), self.eval(node.right)
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '<': lambda a, b: a < b,
                '>': lambda a, b: a > b,
            }
            return ops[node.op](l, r)