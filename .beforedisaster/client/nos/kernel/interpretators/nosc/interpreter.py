from nos.kernel.submodules.dataclasses import *
from nos.modules import instancer as osi


class Interpreter:
    def __init__(self):
        self.fs = osi.fs
        self.env = {}
        self.builtins = {
            'outl':         lambda *args:           print(*args),
            'mkdir':        lambda path:            self.fs.create(path, is_file=False),
            'mkfile':       lambda path:            self.fs.create(path, is_file=True),
            'fdir':         lambda path:            True if self.fs.get(path) is not None else False,
            'modget':       lambda path:            None,
            'input':        lambda prompt='':       input(prompt).strip(),
            'ls':           lambda path='/':        self._ls(path),
            'cat':          lambda path:            self._cat(path),
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

        elif isinstance(node, If):
            result = self.eval(node.condition)
            #print(f'DEBUG if: {node.condition} => {result}')
            if result:
                for stmt in node.body:
                    self.exec(stmt)

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
                '==': lambda a, b: a == b,
            }
            #print('[DEBUG]', ops[node.op](l, r), node.op, (l, r))
            return ops[node.op](l, r)

    def _ls(self, path):
        node = self.fs.get(path)
        if node is None:
            print(f'ls: {path}: No such file or directory')
            return
        for name, child in node.children.items():
            prefix = '/' if not child.is_file else ' '
            print(f'{prefix} {name}')

    def _cat(self, path):
        node = self.fs.get(path)
        if node is None or not node.is_file:
            print(f'cat: {path}: No such file')
            return
        print(node.data.decode('utf-8'))




#===> .nosc DOCS
#
#   | //comment
#   | <variable> <- <value>
#   |
#   | if <expression>
#   |     <to do>
#   |
#   | while <expression>
#   |     <to do>
#   |
#   | each <item> in <collection>
#   |     outl(<item>)
#   |     <to do>
#   |
#   | outl(<text>)  //prints the text or variable value
#   |