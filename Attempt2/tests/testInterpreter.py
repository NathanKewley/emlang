from lib.lexer import Lexer
from lib.parser import Parser
from lib.interpreter import Interpreter
from tests.testBase import TestBase

class TestParser(TestBase):

    def test_interpreter(self):
        source = self.get_file_contents("tests/eml/test_lexer.eml")
        assert self.interpret(source) == """hello
5 is equal to 5
this will not print
statements = 3"""
