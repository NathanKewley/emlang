from lib.lexer import Lexer
from lib.parser import Parser
from tests.testBase import TestBase

class TestParser(TestBase):

    def test_statement_generation(self):
        source = self.get_file_contents("tests/eml/test_lexer.eml")
        lexer = Lexer(source)
        tokens = lexer.lex()
        parser = Parser(tokens)
        statements = parser.parse()
        assert len(statements) == 3
