from lib.lexer import Lexer
from lib.parser import Parser
from lib.interpreter import Interpreter
from tests.testBase import TestBase

class TestControlFlow(TestBase):

    def test_scope(self):
        source = self.get_file_contents("tests/eml/test_scope.eml")
        result = self.get_file_contents("tests/eml/result/test_scope.txt")
        assert self.interpret(source) == result

    def test_if(self):
        source = self.get_file_contents("tests/eml/test_if.eml")
        result = self.get_file_contents("tests/eml/result/test_if.txt")
        assert self.interpret(source) == result    

    def test_for(self):
        source = self.get_file_contents("tests/eml/test_for.eml")
        result = self.get_file_contents("tests/eml/result/test_for.txt")
        assert self.interpret(source) == result                

    def test_while(self):
        source = self.get_file_contents("tests/eml/test_while.eml")
        result = self.get_file_contents("tests/eml/result/test_while.txt")
        assert self.interpret(source) == result           