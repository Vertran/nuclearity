from submodules.interpreter import Interpreter
from submodules.lexer import Lexer
from submodules.parser import Parser

from ..modules.fsys import Filesystem

Filesystem()

tokens = Lexer().start('/home/chlorik/projects/nuclearity/client/os/kernel/def/love_nosc.nosc')

parser = Parser(tokens)
interpreter = Interpreter()

parsed = parser.parse()

interpreter.run(parsed)