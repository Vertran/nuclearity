import re
import struct


class Lexer:
    #==> RegEx
    RULES = [
        ('COMMENT',     r'//[^\n]*'),
        ('FSTRING',     r'f"[^"]*"'),
        ('NAME',        r'[A-Za-z_]\w*'),
        ("NUMBER",      r'\d+'),
        ('ASSIGN',      r'<-'),
        ('STRING',      r'"[^"]*"'),
        ('EQ',          r'=='),
        ('OP',          r'[+\-*/<>().\[\]"\':]'),
        ('NEWLINE',     r'\n'),
        ('INDENT',      r'^( {4})+'),
        ('SKIP',        r'[ ]+'),
        ('EMPTY',       r'^\s*$')
    ]

    #==> keywords
    KEYWORDS = {'IF', 'TRUE', 'FALSE'} #{'each', 'in', 'while', 'modget', 'true', 'false', 'if', 'NaN'}

    #==> binary open
    def open_NOSC_b(self, file_path):
        offset = 0

        with open(file_path, 'rb') as f:
            _file = f.read()

            #=> magic
            #magic = struct.unpack('4sI', _file[:4])
            #offset += 4
            
            #if magic != b'nOSc':
            #    print('not a .nosc file!')
            #    return
                
            #=> header
            #code_len, desc_len, img_len = struct.unpack('4sI', _file[offset:offset+8])
            #offset += 8

            #=> body.code
            #code = struct.unpack(f'{code_len}s', _file[offset:offset+code_len])
            #offset += code_len

            #=> body.desc
            #descriprion = _file[offset:offset+desc_len]
            #offset += desc_len

            #=> body.icon
            #image = _file[offset:offset+img_len]

            #return {
            #    "name": file_path.split('/')[-1][:6],
            #    "description": descriprion,
            #    "code": code,
            #    "icon": image,
            #}
            return _file.decode('utf-8')


    def open_NOSC(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def start(self, text: str):
        #try:
        #    log.info('Interpreting from binary')
        #    code = self.open_NOSC_b(file_path)#['code']
        #except AttributeError:
        #    log.info('Interpreting from opened file')
        #    code = self.open_NOSC(file_path)

        code = text

        #stack = [0]
        tokens = []

        tok_regex = re.compile(
            '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.RULES),
            re.MULTILINE
        )


        for match in re.finditer(tok_regex, code):
            
            kind = match.lastgroup
            value = match.group()

            if kind in ('SKIP', 'EMPTY'):
                continue

            if kind == 'NAME' and value in self.KEYWORDS:
                kind = 'KEYWORD'

            if kind == 'INDENT':
                level = len(value) // 4
                tokens.append(('INDENT', level))
                continue

            tokens.append((kind, value))


        return tokens
