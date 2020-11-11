from lib.lexer import Lexer
from lib.parser import Parser
from lib.interpreter import Interpreter
from tests.testBase import TestBase

class TestParser(TestBase):

    def test_interpreter(self):
        source = self.get_file_contents("tests/eml/test_lexer.eml")
        result = self.get_file_contents("tests/eml/result/test_lexer.txt")
        assert self.interpret(source) == result
