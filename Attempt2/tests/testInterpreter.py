from lib.lexer import Lexer
from lib.parser import Parser
from lib.interpreter import Interpreter
from tests.testBase import TestBase

class TestParser(TestBase):

    def test_token_generation(self):
        source = self.get_file_contents("tests/eml/test_lexer.eml")
        lexer = Lexer(source)
        tokens = lexer.lex()
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter = Interpreter()
        interpreter.interprert(statements)
        assert True
