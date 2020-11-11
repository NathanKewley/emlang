from contextlib import redirect_stdout
import io

from lib.interpreter import Interpreter
from lib.parser import Parser
from lib.lexer import Lexer


class TestBase:
    def get_file_contents(self, test_file):
        file = open(test_file, mode='r')
        source = file.read()
        file.close()
        return source

    def interpret(self, code):
        tokens = Lexer(code).lex()
        statements = Parser(tokens).parse()
        interpreter = Interpreter()

        result = io.StringIO()
        with redirect_stdout(result):
            interpreter.interprert(statements)  
        return result.getvalue()[:-1]
