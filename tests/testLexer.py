from lib.lexer import Lexer
from tests.testBase import TestBase

class TestLexer(TestBase):

    def test_token_generation(self):
        source = self.get_file_contents("tests/eml/test_scope.eml")
        lexer = Lexer(source)
        tokens = lexer.lex()
        assert len(tokens) == 65
