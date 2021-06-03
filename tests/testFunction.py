from lib.lexer import Lexer
from lib.parser import Parser
from lib.interpreter import Interpreter
from tests.testBase import TestBase

class TestFunction(TestBase):

    def test_function(self):
        source = self.get_file_contents("tests/eml/test_function.eml")
        result = self.get_file_contents("tests/eml/result/test_function.txt")
        assert self.interpret(source) == result