from ..dataclasses import *


class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens 
                       if t[0] not in ('COMMENT',)]
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, kind=None):
        tok = self.tokens[self.pos]
        if kind and tok[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {tok}")
        self.pos += 1
        return tok

    def parse(self):
        statements = []
        while self.peek() is not None:
            node = self.parse_statement()
            if node is not None:
                statements.append(node)

        return statements

    def parse_statement(self, level=0):
        while self.peek() and self.peek()[0] == 'NEWLINE':
            self.consume()

        tok = self.peek()

        if tok is None:
            return None

        if tok[0] == 'NAME':
            name = self.consume('NAME')[1]
            if self.peek() and self.peek()[0] == 'ASSIGN':
                self.consume('ASSIGN')
                value = self.parse_expr()
                return Assign(target=name, value=value)

            if self.peek() and self.peek() == ('OP', '('):
                self.consume()
                print(self.peek())
                args = []
                while self.peek() != ('OP', ')'):
                    args.append(self.parse_expr())

                self.consume()
                return Call(func=name, args=args)
            return Name(name)

        # while run
        elif tok == ('KEYWORD', 'while'):
            self.consume()
            cond = self.parse_expr()
            body = self.parse_block(level + 1)
            return While(condition=cond, body=body)

        # each x in y
        elif tok == ('KEYWORD', 'each'):
            self.consume()
            var = self.consume('NAME')[1]
            self.consume()
            iterable = self.parse_expr()
            body = self.parse_block(level + 1)
            return Each(var=var, iterable=iterable, body=body)

        elif tok == ('KEYWORD', 'modget'):
            self.consume()
            path = self.parse_expr()
            return Call(func='modget', args=[path])


        elif tok == ('KEYWORD', 'if'):
            self.consume()
            cond = self.parse_expr()
            body = self.parse_block(level + 1)
            return If(condition=cond, body=body)

        elif tok[0] == 'KEYWORD':
            self.consume()
            return Name(tok[1])

        elif tok[0] == 'NAME':
            return self.parse_expr()

        else:
            self.consume()
            return None

    def parse_expr(self):
        left = self.parse_primary()


        
        while (self.peek() and (self.peek()[0] == 'OP' and self.peek()[1] in ('+', '-', '<', '>')) or self.peek()[0] == 'EQ'):
            op = self.consume()[1]
            right = self.parse_primary()
            left = BinOp(op=op, left=left, right=right)
        
        return left

    def parse_primary(self):
        tok = self.peek()

        if tok[0] == 'STRING':
            self.consume()
            return Literal(tok[1].strip('"'))

        elif tok[0] == 'NUMBER':
            self.consume()
            return Literal(int(tok[1]))

        elif tok[0] == 'FSTRING':
            self.consume()
            return Literal(tok[1])

        elif tok == ('KEYWORD', 'true'):
            self.consume()
            return Literal(True)

        elif tok == ('KEYWORD', 'false'):
            self.consume()
            return Literal(False)

        elif tok[0] == 'NAME':
            name = self.consume()[1]
            if self.peek() and self.peek() == ('OP', '('):
                self.consume()  # (
                args = []
                while self.peek() != ('OP', ')'):
                    args.append(self.parse_expr())
                self.consume()  # )
                return Call(func=name, args=args)
            return Name(name)

    def parse_block(self, level=1):
        body = []
        while self.peek() is not None:
            while self.peek() and self.peek()[0] == 'NEWLINE':
                self.consume()
            if not self.peek() or self.peek()[0] != 'INDENT':
                break
            if self.peek()[1] != level:
                break
            self.consume('INDENT')
            stmt = self.parse_statement(level)
            if stmt:
                body.append(stmt)
        return body